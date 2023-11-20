"""A simple xAmbit API client demonstrating API call + webhook response handling"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import urllib.request
from io import BytesIO
import sys

# Define the local server's port
LOCAL_PORT = 8000
LOCAL_PROXY_URL = "https://<something>.ngrok-free.app"  # grab this using some reverse proxy like ngrok

# Parameters for xAmbit API
# grab these from API documentation
XAMBIT_API_URL = "https://<xAmbit xapp URL>/api/predict"
X_HOST = "<yourdomain>.xambit.io"
X_KEY = "key-<your xambit API key>"


def get_file_bytes(filepath: str) -> BytesIO:
    """Returns file bytes"""
    # assumed to be a PDF file!
    with open(filepath, mode="rb") as ipf:
        data = BytesIO(ipf.read())
    return data


# Define the handler for the HTTP server
class CallbackHandler(BaseHTTPRequestHandler):
    """Handling callback received from xAmbit"""

    def do_POST(self):  # pylint:disable=invalid-name
        """handle post request, print the result"""
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        # Parse JSON
        data = json.loads(post_data)
        # Print JSON
        print(json.dumps(data, indent=4))
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"status": "success"}
        self.wfile.write(json.dumps(response).encode())


def run_server():
    """runs a local server to receive xambit callback"""
    server_address = ("", LOCAL_PORT)
    httpd = HTTPServer(server_address, CallbackHandler)
    print(f"Starting httpd server on port {LOCAL_PORT}")
    httpd.serve_forever()


# Function to send a POST request to the external API
def trigger_xambit_api(filep: str):
    """makes a call to xambit api"""
    # Prepare the payload
    file_data = get_file_bytes(filep)
    payload = {
        "xapp": {
            "xapp": "x-<xapp_id from xambit API doc",
            "template": "t-<template ID from xambit API doc",
        },
        "collection": "",
        "aggregate": True,
        "infer": False,
        "sandbox": "test",
        "hook": {
            "url": LOCAL_PROXY_URL,  # you'll receive callback here
            "method": "POST",
            "headers": {
                "test_key": "test_value",  # you can set any key-values like credentials here
            },
        },
        "file": {
            "blob": list(bytearray(file_data.getvalue())),
            "category": 5,  # internal xambit code for bankstatement category
            "name": "test_bank_statement.pdf",
        },
    }
    payload_data = json.dumps(payload).encode("utf-8")

    # Prepare the request
    req = urllib.request.Request(
        XAMBIT_API_URL,
        data=payload_data,
        headers={"Content-Type": "application/json", "x-host": X_HOST, "x-key": X_KEY},
        method="POST",
    )

    # Send the request
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Initial response from xAmbit API: {response.read().decode()}")
    except urllib.error.URLError as e:
        print(f"Error from xAmbit API: {e.reason}")


# Main function that starts the server and triggers the external API
if __name__ == "__main__":
    print("Usage `python sample_xambit_client.py <path to bank statement pdf>`")
    print("Make sure you are running `ngrok http 8000` before calling this app")
    print("Set the ngrok URL in `LOCAL_PROXY_URL` at the top of this file")
    filepath = sys.argv[1]
    # Start the server in a new thread
    server_thread = threading.Thread(target=run_server)
    # server_thread.daemon = True
    server_thread.start()

    # Trigger the external API call
    trigger_xambit_api(filepath)

    # Keep the main thread alive
    server_thread.join(timeout=900)  # 15 minutes wait

    if server_thread.is_alive():
        print("could not receive response from xambit")
        sys.exit(1)
    sys.exit(0)
