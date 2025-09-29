import os
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from listeners import register_listeners

# Initialization
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
logging.basicConfig(level=logging.DEBUG)

# Native Python HTTP health check server
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        else:
            self.send_response(404)
            self.end_headers()

# Register Listeners
register_listeners(app)

# Start Bolt app


def run_health_server():
    port = int(os.environ.get("HEALTH_PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

if __name__ == "__main__":
    # Start native health check server in a separate thread
    threading.Thread(target=run_health_server, daemon=True).start()
    # Start Slack Bolt app
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
