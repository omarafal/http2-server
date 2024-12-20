import socket
import ssl
import h2
from h2.config import H2Configuration
from h2.connection import H2Connection

forbidden=["/for.html"]

def handle_connection(sock):
    conn = H2Connection(H2Configuration(client_side=False))
    conn.initiate_connection()
    sock.sendall(conn.data_to_send())

    while True:
        data = sock.recv(65535)
        if not data:
            break

        events = conn.receive_data(data)
        for event in events:
            if isinstance(event, h2.events.RequestReceived):
                # Handle HTTP/2 request
                stream_id = event.stream_id
                response_headers = [
                    (':status', '200 OK'),
                    ('content-type', 'text/plain'),
                ]
                # print(event)
                
                # parse header content
                # Initialize a dictionary to store the parsed headers
                parsed_headers = {}

                # Iterate through the header list and parse each tuple
                for key, value in event.headers:
                    parsed_headers[key.decode()] = value.decode()

                # Print the parsed headers
                for path in forbidden:
                    if parsed_headers[":path"] == path:

                        response_headers = [
                            (':status', '403 Forbidden'),
                            # ('content-type', 'text/plain'),
                        ]
                
                conn.send_headers(stream_id, response_headers, end_stream=False)


                # for key, value in parsed_headers.items():
                #     print(f"{key}: {value}")

                with open("index.html") as file:
                    text = file.read()
                
                conn.send_data(stream_id, text.encode(), end_stream=True)
                
                # if conn.streams[stream_id].state == 'open':
                        # conn.end_stream(event.stream_id)

        sock.sendall(conn.data_to_send())

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
    print(f"HTTP/2 Server running on https://{HOST}:{PORT}")
    while True:
        client_sock, _ = server.accept()
        print("Client connected.")
        with context.wrap_socket(client_sock, server_side=True) as tls_sock:
            handle_connection(tls_sock)
