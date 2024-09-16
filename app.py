import socketserver
import http.server
import ssl
import threading
from flask import Flask, render_template_string

# Flask app for serving the HTML status page
app = Flask(__name__)

# HTML template for the status page
status_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Server Status</title>
</head>
<body>
    <h1>Proxy Server Status</h1>
    <p>The proxy server is running on port 8888 with SSL encryption.</p>
    <p>Everything looks good!</p>
</body>
</html>
"""

@app.route('/')
def status():
    return render_template_string(status_page)

# Proxy server handler
class Proxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Proxy functionality can be added here
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Proxy server is running with SSL encryption.")

    def do_CONNECT(self):
        self.send_response(200)
        self.end_headers()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

# Run proxy server on port 8888 with SSL
def run_proxy_server(host='0.0.0.0', port=8888, certfile="cert.pem", keyfile="key.pem"):
    with ThreadedTCPServer((host, port), Proxy) as server:
        # Wrap the socket with SSL
        server.socket = ssl.wrap_socket(server.socket, certfile=certfile, keyfile=keyfile, server_side=True)
        print(f"Serving proxy with SSL on {host}:{port}")
        server.serve_forever()

# Run Flask server on port 80
def run_status_server():
    app.run(host='0.0.0.0', port=80)

if __name__ == "__main__":
    # Start the proxy server in a separate thread
    proxy_thread = threading.Thread(target=run_proxy_server)
    proxy_thread.daemon = True
    proxy_thread.start()

    # Start the Flask server on port 80
    run_status_server()
