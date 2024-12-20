import socket
import h2
from h2.connection import H2Connection
from h2.config import H2Configuration
import request
from datetime import datetime
from misc import *
from random import randint

global cl_id

def handle_connection(sock):
    # Initialize HTTP/2 connection
    conn = H2Connection(H2Configuration(client_side=False))
    conn.initiate_connection()
    sock.sendall(conn.data_to_send())

    mainBreak = True

    while mainBreak:
        try:
            data = sock.recv(65535)
            if not data:
                break

            events = conn.receive_data(data)
            for event in events:
                if isinstance(event, h2.events.RequestReceived):
                    stream_id = event.stream_id
                    req = request.handle_request(event)
                    conn.send_headers(stream_id, req[0], end_stream=False)
                    conn.send_data(stream_id, req[1][1], end_stream=True)
                elif isinstance(event, h2.events.StreamEnded):
                    conn.close_connection()
                    mainBreak = False

            sock.sendall(conn.data_to_send())
        except ConnectionResetError:
            print_cmd("A connection reset happened.")
            break

HOST = '127.0.0.1'

try:
    PORT = 8080
except OSError:
    PORT = 8081

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as server:
    server.bind((HOST, PORT))
    server.listen(5)
    print_cmd(f"HTTP/2 Server running on http://{HOST}:{PORT}")

    # socket.setdefaulttimeout(2)

    while True:
        cl_id = randint(0, 5)
        client_sock, _ = server.accept()
        print_cmd("Client connected.")
        handle_connection(client_sock)
        client_sock.close()
