import socket
import ssl
from main_serv import main

def alpn():
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8443))
    server_socket.listen(1)

    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="certs/server.crt", keyfile="certs/server.key")  # Use your certificate and key
    context.set_alpn_protocols(["h2", "http/1.1"])  # Supported protocols

    print("Server is listening on port 8443...")

    # Accept a connection and wrap it with SSL
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address}")
        try:
            with context.wrap_socket(client_socket, server_side=True) as tls_socket:
                selected_protocol = tls_socket.selected_alpn_protocol()
                print(f"ALPN Protocol Negotiated: {selected_protocol}")

                # # Wait for an HTTP request
                # request = tls_socket.recv(1024).decode('utf-8')
                # print("Request received:")
                # print(request)

                # # Send a basic HTTP response
                # response = (
                #     "HTTP/2.0 200 OK\r\n"
                #     "Content-Type: text/html\r\n"
                #     "Content-Length: 19\r\n"
                #     "\r\n"
                #     "Hello from the server!"
                # )
                # tls_socket.sendall(response.encode('utf-8'))

                main(tls_socket)

        except ssl.SSLError as e:
            print(f"SSL Error: {e}")
        finally:
            client_socket.close()

# Run the server
alpn()
