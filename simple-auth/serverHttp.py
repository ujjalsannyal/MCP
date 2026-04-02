#!/usr/bin/env python3
"""
Simple HTTP Server in Python
Usage: python http_server.py [port]
Default port: 8080
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
from datetime import datetime


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            json_data = {"message": "Hello from Python HTTP Server!"}
            self.wfile.write(json.dumps(json_data))

        elif self.path == "/health":
            self.send_json(200, {"status": "ok", "timestamp": datetime.now().isoformat()})

        else:
            self.send_json(404, {"error": "Not Found", "path": self.path})

    def do_POST(self):
        """Handle POST requests."""
        if self.path == "/echo":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body)
                self.send_json(200, {"echo": data})
            except json.JSONDecodeError:
                self.send_json(400, {"error": "Invalid JSON body"})

        else:
            self.send_json(404, {"error": "Not Found", "path": self.path})

    def send_json(self, status_code, data):
        """Helper to send a JSON response."""
        response = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {self.address_string()} - {format % args}")


def run(port=8080):
    server_address = ("", port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"🚀 Server started at http://localhost:{port}")
    print("   Press Ctrl+C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
        httpd.server_close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run(port)