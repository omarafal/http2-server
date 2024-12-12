import socket
import ssl
import h2
from h2.connection import H2Connection
from h2.config import H2Configuration
import headers
from datetime import datetime
from misc import *

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

    while True:
        try:
            data = sock.recv(65535) # This is the raw binary data coming from the client over the network in bytes.
            if not data:
                break

            events = conn.receive_data(data)
            for event in events:
                if isinstance(event, h2.events.RequestReceived):
                    # Send response headers
                    stream_id = event.stream_id
                    
                    conn.send_headers(stream_id, headers.handle_request(event), end_stream=False)

                    # Read and send the requested document (defaulting to index.html)
                    try:
                        with open("index.html", "r") as file:
                            content = file.read()
                    except FileNotFoundError:
                        content = "<h1>404 Not Found</h1>"

                    conn.send_data(stream_id, content.encode(), end_stream=True)

            sock.sendall(conn.data_to_send())
        
        except ConnectionResetError:
            print_cmd("Connection forcibly closed by client.")
            break # break for now, put handle later
            #NOTE: for some reason, after breaking it still listens and sends information
            #Another NOTE: Figured it out, it's because there is a while loop in with socket.socket

# Set up SSL for HTTP/2
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_3
context.set_ciphers("ECDHE+AESGCM")
context.load_cert_chain(certfile="server.crt", keyfile="server.key")
context.set_alpn_protocols(["h2"])

HOST = '127.0.0.1'
PORT = 8442

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as server:
    server.bind((HOST, PORT))
    server.listen(5)
    print_cmd(f"HTTP/2 Server running on https://{HOST}:{PORT}")

    while True:
        client_sock, _ = server.accept()
        print_cmd("Client connected.")
        with context.wrap_socket(client_sock, server_side=True) as tls_sock:
            handle_connection(tls_sock)