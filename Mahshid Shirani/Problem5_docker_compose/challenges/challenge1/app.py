# challenge1/app.py
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"FLAG{challenge1_dummy_flag}")

if __name__ == "__main__":
    server = HTTPServer(('', 1337), Handler)
    print("Challenge 1 running on port 1337...")
    server.serve_forever()
