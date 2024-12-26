import socket
import ssl
from main_serv import main
# from main_serv_copy import main
from misc import *

def alpn():
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8443))
    server_socket.listen(1)

    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="certs/server.crt", keyfile="certs/server.key")
    context.set_alpn_protocols(["h2", "http/1.1"])

    print("Server is listening on port 8443...")

    # Accept a connection and wrap it with SSL
    while True:
        client_socket, address = server_socket.accept()
        print_cmd(f"Connection from {address}")
        try:
            with context.wrap_socket(client_socket, server_side=True) as tls_socket:
                selected_protocol = tls_socket.selected_alpn_protocol()
                print_cmd(selected_protocol, "ALPN Protocol Negotiated")

                main(tls_socket)
                print_cmd("CLOSING CONNECTION")

        except ssl.SSLError as e:
            print(f"SSL Error: {e}")
        finally:
            client_socket.close()

alpn()
