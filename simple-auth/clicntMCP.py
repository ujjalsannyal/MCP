
# valid_token = "valid-token123"

# async with streamablehttp_client(
#         url = f"http://localhost:{port}/mcp",
#         headers = {"Authorization": f"Bearer {valid_token}"}
#     ) as (
#         read_stream,
#         write_stream,
#         session_callbackye
#     ):
#         async with clientSession(
#                 read_stream,
#                 write_stream,
#         ) as session:
#                 await session.initialize()
#                 response = await session.get("/resource")
#                 print("Response status:", response.status)
#                 print("Response body:", await response.text())


import asyncio

import httpx
from fastmcp import Client
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def login_and_get_token():
    # Simulate login to get JWT token
    # In a real scenario, you would make an HTTP request to the /auth/token endpoint
    # with valid credentials and receive a JWT token in response.
    async with httpx.AsyncClient() as http:
        response = await http.post('http://localhost:8000/auth/token', json={'username': 'alice', 'password': 'password123'})
        return response.json()['access_token']

async def main():
    token = await login_and_get_token()
    print("Obtained JWT token:", token)
    # async with httpx.AsyncClient(headers={"Authorization": f"Bearer {token}"}) as http:
    async with Client(
        "http://localhost:8000/mcp",
        auth=token
    ) as client:
        # client.set_headers({"Authorization": f"Bearer {token}"})  # Set the Authorization header with the JWT token
        # initialize + session ID managed automatically ✅
        tools = await client.list_tools()
        result = await client.call_tool("greet", {"name": "Alice"})
        print(result)
    # async with httpx.AsyncClient(headers={"Authorization": f"Bearer {token}"}) as http:
    #     async with streamable_http_client(
    #         url = "http://localhost:8000/mcp/",
    #         http_client = http
    #     ) as (
    #         read_stream,
    #         write_stream,
    #         session_callbackye
    #     ):
    #         async with ClientSession(
    #                 read_stream,
    #                 write_stream,
    #         ) as session:
    #                 await session.initialize()
    #                 response = await session.get("/resource")
    #                 print("Response status:", response.status)
    #                 print("Response body:", await response.text())

asyncio.run(main())