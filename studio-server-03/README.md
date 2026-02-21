# MCP Server Configuration

This directory contains an MCP (Model Context Protocol) server implementation with configuration files.

## Server Details

**Name:** example-stdio-server  
**Transport:** stdio  
**Language:** Python

## Available Tools

1. **get_greeting** - Generate a personalized greeting
   - Input: `name` (string)
   - Returns: Personalized greeting message

2. **calculate_sum** - Calculate the sum of two numbers
   - Input: `a` (number), `b` (number)
   - Returns: Sum of a and b

3. **calculate_product** - Calculate the product of two numbers
   - Input: `a` (number), `b` (number)
   - Returns: Product of a and b

4. **get_server_info** - Get information about this MCP server
   - Input: None
   - Returns: Server metadata (name, version, transport, capabilities)

## Configuration Files

### `mcp-config.json`
This is the MCP configuration file that can be used by MCP clients to connect to the server.

**Usage with Claude Desktop:**

1. Locate your Claude Desktop configuration file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. Copy the contents of `mcp-config.json` and merge it into your Claude Desktop config file under the `mcpServers` key.

3. Restart Claude Desktop.

**Example merged configuration:**
```json
{
  "mcpServers": {
    "example-stdio-server": {
      "command": "python",
      "args": [
        "src/server/server.py"
      ],
      "cwd": "/Users/ujjalsannyal/Documents/workspace/MCP/studio-server-03",
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

## Running the Server

### Using MCP Inspector (for testing)
```bash
npx @modelcontextprotocol/inspector python src/server/server.py
```

### Direct execution
```bash
python src/server/server.py
```

## Requirements

- Python 3.10+
- MCP Python SDK (`mcp` package)

Install dependencies:
```bash
pip install mcp
```

## Project Structure

```
studio-server-03/
├── src/
│   └── server/
│       └── server.py          # Main server implementation
├── mcp-config.json            # MCP configuration file
├── package.json               # Node.js dependencies (for inspector)
└── README.md                  # This file
```

## Environment Variables

- `PYTHONUNBUFFERED=1` - Ensures Python output is not buffered (important for stdio transport)

## Troubleshooting

### Server not appearing in Claude Desktop
1. Check that the path in `cwd` is correct and absolute
2. Verify Python is in your PATH
3. Check Claude Desktop logs for errors
4. Restart Claude Desktop after configuration changes

### Tools not working
1. Verify the server is running with the MCP Inspector
2. Check that tool schemas match the expected format
3. Review server logs for errors

## Development

To modify the server:
1. Edit `src/server/server.py`
2. Update tool definitions in the `list_tools()` handler
3. Update tool implementations in the `call_tool()` handler
4. Test with MCP Inspector before deploying to Claude Desktop

## License

ISC
