import socket
import ssl
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
    """
    This sends the initial HTTP/2 preface, which is a required
    sequence of bytes that both client and server exchange to start the protocol.
    """
    conn.initiate_connection()

    # function to send to client the provided data in arg
    sock.sendall(conn.data_to_send())

    mainBreak = True

    while mainBreak:
        try:
            data = sock.recv(65535) # This is the raw binary data coming from the client over the network in bytes.
            if not data:
                break

            events = conn.receive_data(data)
            for event in events:
                # print(f"EVENT {event}")
                if isinstance(event, h2.events.RequestReceived):
                    # Send response headers
                    stream_id = event.stream_id

                    # NOTE: Use this variable instead of calling the function again and again
                    req = request.handle_request(event)
                    
                    conn.send_headers(stream_id, req[0], end_stream=False)
                    
                    conn.send_data(stream_id, req[1][1], end_stream=True)
                elif isinstance(event, h2.events.StreamEnded):
                    # end connection
                    conn.close_connection()
                    mainBreak = False

            sock.sendall(conn.data_to_send())
            
            # sock.cl
        except:
            if ConnectionResetError:
                print_cmd("A connection reset happened.")
                break
    
# Set up SSL for HTTP/2
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_3
context.set_ciphers("ECDHE+AESGCM")
context.load_cert_chain(certfile="server.crt", keyfile="server.key")
context.set_alpn_protocols(["h2"])

HOST = '127.0.0.1'

try:
    PORT = 8443
except OSError:
    PORT = 8442

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as server:
    server.bind((HOST, PORT))
    server.listen(5)
    print_cmd(f"HTTP/2 Server running on https://{HOST}:{PORT}")

    socket.setdefaulttimeout(2) # set timeout incase it stucks

    while True:
        cl_id = randint(0, 5)
        client_sock, _ = server.accept()
        # while True:
        print_cmd("Client connected.")
        with context.wrap_socket(client_sock, server_side=True) as tls_sock:
            handle_connection(tls_sock)
            # client_sock.close()