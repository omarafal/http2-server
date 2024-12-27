import socket
import ssl
import threading
from main_serv import main
from misc import *
import sys


def handle_client(tls_socket, address, log):
    """
    Function to handle a single client connection.
    """
    print_cmd(log=log, data="Connection from {address}")
    try:
        selected_protocol = tls_socket.selected_alpn_protocol()
        print_cmd(log,selected_protocol, "ALPN Protocol Negotiated")

        # Pass the connection to the main server logic
        main(tls_socket, log)
        print_cmd(data="CLOSING CONNECTION",log=log)
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
    # except Exception as e:
    #     print(f"Error handling client: {e}")
    finally:
        tls_socket.close()


def alpn(log):
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8443))
    server_socket.listen(5)  # Allow up to 5 pending connections

    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="certs/server.crt", keyfile="certs/server.key")
    context.set_alpn_protocols(["h2", "http/1.1"])

    print(f"Server is listening on port 8443...")

    while True:
        # Accept a connection
        client_socket, address = server_socket.accept()
        try:
            tls_socket = context.wrap_socket(client_socket, server_side=True)
        except ssl.SSLError as e:
            print(f"SSL Error during handshake: {e}")
            client_socket.close()
            continue

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(tls_socket, address, log))
        client_thread.daemon = True  # Allow server to exit even if threads are running
        client_thread.start()

# alpn()

# if __name__ == "__main__":
#     alpn()
