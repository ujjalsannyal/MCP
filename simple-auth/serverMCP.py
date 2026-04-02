import math

from fastmcp import FastMCP
from JWTPermissionMiddleware import JWTPermissionMiddleware, login
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import Route, Mount

# Settings configuration
settings = {
    "host": "127.0.0.1",
    "port": 8000,
    "log_level": "INFO"
}

# creating MCP Server
app = FastMCP(
    name="MCP Resource Server",
    instructions="Resource Server that validates tokens via Authorization Server introspection",
)

middleware = [
    Middleware(JWTPermissionMiddleware)
]

mcpApp=app.http_app(path='/')

# creating starlette web app
starlette_app = Starlette(
    lifespan=mcpApp.lifespan,
    routes = [
        Route("/auth/token", login, methods=["POST"]),
        Mount("/mcp", mcpApp)
    ],
    middleware=middleware
)

# ─────────────────────────────────────────────
# Tools  (functions the AI can call)
# ─────────────────────────────────────────────

@app.tool()
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"

@app.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b
 
 
@app.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b
 
 
@app.tool()
def square_root(number: float) -> float:
    """Return the square root of a number."""
    if number < 0:
        raise ValueError("Cannot take square root of a negative number.")
    return math.sqrt(number)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(starlette_app, host="127.0.0.1", port=8000)
    