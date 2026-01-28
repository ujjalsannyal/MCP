import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Create an MCP server
const server = new McpServer({
  name: "Demo",
  version: "1.0.0"
});




// Add an addition tool
server.tool("add",
  "Add two numbers together",
  { a: z.number(), b: z.number() },
  async ({ a, b }) => ({
    content: [{ type: "text", text: String(a + b) }]
  })
);

server.tool("divide",
  "Divide two numbers together",
  { a: z.number(), b: z.number() },
  async ({ a, b }) => ({
    content: [{ type: "text", text: String(a / b) }]
  })
);

server.tool("multiply",
  "Multiply two numbers together",
  { a: z.number(), b: z.number() },
  async ({ a, b }) => ({
    content: [{ type: "text", text: String(a * b) }]
  })
);

server.tool("subtract",
  "Subtract two numbers together",
  { a: z.number(), b: z.number() },
  async ({ a, b }) => ({
    content: [{ type: "text", text: String(a - b) }]
  })
);

server.registerTool("help",{
  title: "Help Tool",
  description: "help you with available operations"
  },
  async () => ({
    content: [{ type: "text" as const, text: `Available operations: add, subtract, multiply, divide` }]
  })
);

// Add a dynamic greeting resource
server.resource(
    "readFile",
    new ResourceTemplate("file://{name}", { list: undefined }),
    async (uri, { name }) => ({
      contents: [{
        uri: uri.href,
        text: `Hello, ${name}!`
      }]
    })
);

server.prompt(
    "review-code",
    { code: z.string() },
    ({ code }) => ({
        messages: [{
        role: "user",
        content: {
            type: "text",
            text: `Please review this code:\n\n${code}`
        }
        }]
    })
);

// Start receiving messages on stdin and sending messages on stdout

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCPServer started on stdin/stdout");
}

main().catch((error) => {
  console.error("Fatal error: ", error);
  process.exit(1);
});