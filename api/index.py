# api/index.py - Minimal test
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        message = {
            "status": "working",
            "path": self.path,
            "message": "If you see this, the API is deployed!"
        }
        
        self.wfile.write(json.dumps(message).encode())
        return