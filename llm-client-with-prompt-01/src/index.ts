import { McpServer, ResourceTemplate } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

const server = new McpServer({
    name: 'Calculator MCP Server',
    version: '1.0.0',
});

// Define a simple addition resource
server.tool(
    "add",
    "Add two numbers together",
    { a: z.number(), b: z.number() },
    async ({ a, b }) => ({
        content: [{ type: 'text', text: String(a + b) }],
    })
)

server.tool(
    "Multiply",
    "Multyply two numbers together",
    { a: z.number(), b: z.number() },
    async ({ a, b }) => ({
        content: [{ type: 'text', text: String(a * b) }],
    })
)

server.tool(
    "subtract",
    "Subtract two numbers together",
    { a: z.number(), b: z.number() },
    async ({ a, b }) => ({
        content: [{ type: 'text', text: String(a - b) }],
    })
)

server.tool(
    "divide",
    "Divide two numbers together",
    { a: z.number(), b: z.number() },
    async ({ a, b }) => ({
        content: [{ type: 'text', text: String(a / b) }],
    })
)

server.resource(
    "greetings",
    new ResourceTemplate("greeting:/{name}", { list: undefined }),
    async (uri, { name }) => ({
        contents: [{
            uri: uri.href,
            text: `Hello, ${name}!`
        }]
    })
);

const transport = new StdioServerTransport();
server.connect(transport);