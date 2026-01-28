import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { Transport } from "@modelcontextprotocol/sdk/shared/transport.js";
import OpenAI from "openai";
import { z } from "zod"; // Import zod for schema validation
import dotenv from "dotenv";

// Load environment variables from develop.env file
dotenv.config({ path: "./develop.env" });

class MCPClient {
  private openai: OpenAI;
  private client: Client;
  constructor() {
    const githubToken = process.env.GITHUB_TOKEN;

    if (!githubToken) {
      throw new Error(
        "GITHUB_TOKEN environment variable is not set. " +
        "Please set it before running the client: export GITHUB_TOKEN=your_token_here"
      );
    }

    this.openai = new OpenAI({
      baseURL: "https://models.inference.ai.azure.com",
      apiKey: githubToken,
    });

    this.client = new Client(
      {
        name: "example-client",
        version: "1.0.0",
      },
      {
        capabilities: {
          experimental: {},
          sampling: {},
          elicitation: {},
          roots: {},
        },
      }
    );
  }

  async connectToServer(transport: Transport) {
    await this.client.connect(transport);
    this.run();
    console.error("MCPClient started on stdin/stdout");
  }

  async run() {
    console.log("Asking server for available tools");

    // listing tools
    const toolsResult = await this.client.listTools();
    const tools = toolsResult.tools.map((tool) => this.openAiToolAdapter({
      name: tool.name,
      description: tool.description,
      input_schema: tool.inputSchema,
    }));
    console.log("Tools:", tools);

    // 1. Create messages that's input for the LLM
    const prompt = "What is the sum of 2 and 3?";

    const messages: OpenAI.Chat.Completions.ChatCompletionMessageParam[] = [
      {
        role: "user",
        content: prompt,
      },
      {
        role: "user",
        content: "what is 2 times 3?",
      },
      {
        role: "user",
        content: "subtract 2 and 3?",
      },
      {
        role: "user",
        content: "What is the quotient of 2 and 3?",
      },
    ];

    console.log("Querying LLM: ", messages[0].content);
    let response = this.openai.chat.completions.create({
      model: "gpt-4o-mini",
      max_tokens: 1000,
      messages,
      tools: tools,
    });

    let results: any[] = [];

    // 1. Go through the LLM response,for each choice, check if it has tool calls 
    (await response).choices.map(async (choice: { message: any; }) => {
      const message = choice.message;
      if (message.tool_calls) {
        console.log("Making tool call")
        await this.callTools(message.tool_calls, results);
      }
    });
  }

  openAiToolAdapter(tool: {
    name: string;
    description?: string;
    input_schema: any;
  }) {
    // Create a zod schema based on the input_schema
    const schema = z.object(tool.input_schema);

    return {
      type: "function" as const, // Explicitly set type to "function"
      function: {
        name: tool.name,
        description: tool.description,
        parameters: {
          type: "object",
          properties: tool.input_schema.properties,
          required: tool.input_schema.required,
        },
      },
    };
  }

  async callTools(tool_calls: OpenAI.Chat.Completions.ChatCompletionMessageToolCall[], toolsResult: any[]) {
    for (const tool_call of tool_calls) {
      if (tool_call.type === "function") {
        const toolName = tool_call.function.name;
        const toolArgs = tool_call.function.arguments;

        console.log(`Calling tool: ${toolName} with arguments: ${toolArgs} `);

        // 2. Call the server's tool 
        const toolResult = await this.client.callTool({
          name: toolName,
          arguments: JSON.parse(toolArgs),
        });

        console.log("Tool result: ", toolResult);

        // 3. Do something with the result
        // TODO 
      }


    }
  }
}

let client = new MCPClient();
const transport = new StdioClientTransport({
  command: "node",
  args: ["./build/index.js"]
});

client.connectToServer(transport);