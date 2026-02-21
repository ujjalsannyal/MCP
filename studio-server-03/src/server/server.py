import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the server
server = Server("example-stdio-server")

# Define available tools
@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools"""
    return [
        Tool(
            name="get_greeting",
            description="Generate a personalized greeting",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name to greet"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="calculate_sum",
            description="Calculate the sum of two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="calculate_product",
            description="Calculate the product of two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="get_server_info",
            description="Get information about this MCP server",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

# Handle tool calls
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution"""
    if name == "get_greeting":
        breakpoint()  # Debugger stops here
        greeting = f"Hello, {arguments['name']}! Welcome to MCP stdio server."
        return [TextContent(type="text", text=greeting)]
    
    elif name == "calculate_sum":
        result = arguments['a'] + arguments['b']
        return [TextContent(type="text", text=str(result))]
    
    elif name == "calculate_product":
        result = arguments['a'] * arguments['b']
        return [TextContent(type="text", text=str(result))]
    
    elif name == "get_server_info":
        info = {
            "server_name": "example-stdio-server",
            "version": "1.0.0",
            "transport": "stdio",
            "capabilities": ["tools"]
        }
        return [TextContent(type="text", text=str(info))]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())