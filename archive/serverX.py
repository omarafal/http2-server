import socket
import base64
from misc import *
from server_parse_req import *

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 8080         # Port to listen on

# HTML response to serve
HTML_RESPONSE = """HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
    <title>Simple HTTP Server</title>
</head>
<body>
    <h1>Welcome to the Simple HTTP Server!</h1>
    <p>This is a basic HTTP 1.1 server implemented in Python.</p>
</body>
</html>
"""

def get_fields(req):
    fields = {}
    for field in  req.split("\r\n")[:len(req.split("\r\n"))-1]:
        fields[field.split(":")[0]] = field.split(":")[1].strip()

    return fields



def preface(req):
    """
    Function to handle incoming ALPN
    """
    # fields = get_fields(req)
    pre_headers = {
        "status": "HTTP/1.1 101 Switching Protocols",
        "Connection": "Upgrade",
        "Upgrade": "h2c",
    }

    return pre_headers

# store stream IDs
active_users = []

def start_server():
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)  # Listen for up to 5 connections

        print(f"Server started on http://{HOST}:{PORT}")

        while True:
            # Accept a connection
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Connection received from {client_address}")

                # Receive the request data
                request = client_socket.recv(1024).decode('utf-8')

                # start with alpn (server-side)
                step1 = make_frame(preface(request))
                print_cmd(request, "REQUEST RECEIVED")
                print(f"Request: {request}")
                client_socket.sendall(step1.encode('utf-8'))

                fields = get_fields(request)
                print_cmd(b64_decode(fields["HTTP2-Settings"]))
                

                # Send the HTTP response
                # client_socket.sendall(HTML_RESPONSE.encode('utf-8'))



if __name__ == "__main__":
    start_server()