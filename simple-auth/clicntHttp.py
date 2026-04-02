
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


#!/usr/bin/env python3
"""
HTTP Client for consuming the Python HTTP Server.
Usage: python http_client.py [base_url]
Default base URL: http://localhost:8080
"""

import json
import sys
import urllib.request
import urllib.error
from datetime import datetime


BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"


# ─────────────────────────────────────────────
# Core request helper
# ─────────────────────────────────────────────

def request(method: str, path: str, payload: dict = None):
    """Send an HTTP request and return (status_code, body)."""
    url = f"{BASE_URL}{path}"
    data = json.dumps(payload).encode("utf-8") if payload else None
    headers = {"Content-Type": "application/json"} if data else {}

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            raw = response.read().decode("utf-8")
            content_type = response.headers.get("Content-Type", "")
            body = json.loads(raw) if "application/json" in content_type else raw
            return response.status, body

    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        try:
            body = json.loads(raw)
        except json.JSONDecodeError:
            body = raw
        return e.code, body

    except urllib.error.URLError as e:
        print(f"\n❌ Could not connect to {BASE_URL}")
        print(f"   Reason: {e.reason}")
        print("   Make sure http_server.py is running.\n")
        sys.exit(1)


# ─────────────────────────────────────────────
# Pretty printer
# ─────────────────────────────────────────────

def print_response(label: str, status: int, body):
    icon = "✅" if 200 <= status < 300 else "❌"
    print(f"\n{icon}  [{label}]  HTTP {status}")
    print("─" * 45)
    if isinstance(body, dict):
        print(json.dumps(body, indent=2))
    else:
        # Trim long HTML for readability
        preview = body[:300] + "..." if len(body) > 300 else body
        print(preview)
    print()


# ─────────────────────────────────────────────
# Individual API calls
# ─────────────────────────────────────────────

def get_home():
    status, body = request("GET", "/")
    print_response("GET /", status, body)


def get_health():
    status, body = request("GET", "/health")
    print_response("GET /health", status, body)


def get_info():
    status, body = request("GET", "/info")
    print_response("GET /info", status, body)


def post_echo(payload: dict):
    status, body = request("POST", "/echo", payload)
    print_response("POST /echo", status, body)


def get_not_found():
    status, body = request("GET", "/this-does-not-exist")
    print_response("GET /unknown (404 demo)", status, body)


# ─────────────────────────────────────────────
# Run all calls
# ─────────────────────────────────────────────

def main():
    print("=" * 45)
    print(f"  HTTP Client — {BASE_URL}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 45)

    get_home()
    get_health()
    get_info()
    post_echo({"message": "Hello, Server!", "timestamp": datetime.now().isoformat()})
    get_not_found()

    print("=" * 45)
    print("  All requests completed.")
    print("=" * 45)


if __name__ == "__main__":
    main()
