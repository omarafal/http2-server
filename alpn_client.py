import ssl
import socket

def alpn_client():
    # Create a socket
    client_socket = socket.create_connection(('localhost', 8443))

    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cafile="certs/ca.crt")  # Use your CA certificate
    context.set_alpn_protocols(["h2", "http/1.1"])  # Desired protocols

    # Wrap the socket with SSL
    with context.wrap_socket(client_socket, server_hostname="localhost") as tls_socket:
        selected_protocol = tls_socket.selected_alpn_protocol()
        print(f"ALPN Protocol Negotiated: {selected_protocol}")

        # Send a basic HTTP response
        request = "PLEAS HE"
        tls_socket.sendall(request.encode('utf-8'))


        # Receive data from the server
        data = tls_socket.recv(1024)
        print(f"Received: {data.decode()}")

# Run the client
alpn_client()
