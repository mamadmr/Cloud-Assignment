# challenge2/app.py
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"FLAG{challenge2_dummy_flag}")

if __name__ == "__main__":
    server = HTTPServer(('', 1338), Handler)
    print("Challenge 2 running on port 1338...")
    server.serve_forever()
