import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

APP_VERSION = os.getenv("APP_VERSION", "v1 (STABLE)")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        hostname = socket.gethostname()
        body = f"Python Canary App | Version: {APP_VERSION} | Pod: {hostname}\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, format, *args):
        print(f"[{APP_VERSION}] {self.address_string()} - {format % args}", flush=True)

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print(f"Starting server on port 8080 ({APP_VERSION})...", flush=True)
    server.serve_forever()