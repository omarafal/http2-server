import socket
from random import randint
import sys
import base64
from misc import *

HOST = sys.argv[1]  # Target host
PORT = int(sys.argv[2])  # HTTP port

# init stream id
stream_id = 1

# initial HTTP request to send

def init_conn():
    pass

# 
# pre-face & settings


# """GET / HTTP/1.1
# Host: example.com
# Connection: close


# """

def alpn_preface(settings_op):

    """
    Function to initialize the ALPN
    """

    settings_b64 = base64.b64encode(settings_op)

    alpn_headers = {
        "GET": "/ HTTP/1.1",
        "Host": f"{HOST}",
        "Connection": "upgrade",
        "Upgrade": "http/2.0",
        "HTTP2-Settings": f"{settings_b64}" 
    }

    return alpn_headers

settings = b"SETTINGS_ENABLE_PUSH = 1"

alpn_preface(settings)

def send_request():
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        # HTTP_REQUEST = make_req(init_req)
        
        print(f"Sending request to {HOST}:{PORT}")

        # START WITH ALPN (client-side)
        step1 = make_frame(alpn_preface(settings))
        print_cmd(step1, "INITIALIZE ALPN")
        client_socket.sendall(step1.encode('utf-8'))

        # Send the HTTP request

        # Receive the HTTP response
        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        response = response.decode('utf-8')
        print_cmd(response, "RESPONSE RECEIVED:")

        # SEND REQUEST
        req1_headers = {
            "GET": "/ HTTP/2.0",
            "Host": f"{HOST}",
            "Connection": "keep-alive",
            "Stream-id": f"{stream_id}",

        }

if __name__ == "__main__":
    send_request()
