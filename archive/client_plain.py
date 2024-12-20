import socket
import h2
import hyperframe.frame as hf
from h2.config import H2Configuration
from h2.connection import H2Connection
from h2.events import ResponseReceived, DataReceived
import sys

def run_http2_client(host, port):
    # Create a standard socket connection
    with socket.create_connection((host, port)) as sock:
        # Initialize the HTTP/2 connection
        config = H2Configuration(client_side=True)
        conn = H2Connection(config)
        conn.initiate_connection()
        sock.sendall(conn.data_to_send())

        # Send an HTTP/2 request
        request_headers = [
            (":method", "GET"),
            (":scheme", "http"),  # Changed from "https" to "http"
            (":authority", host),
            (":path", "/for.html"),
        ]
        conn.send_headers(stream_id=1, headers=request_headers, end_stream=False)
        sock.sendall(conn.data_to_send())

        # Receive and process the response
        while True:
            data = sock.recv(65535)
            if not data:
                break

            events = conn.receive_data(data)
            for event in events:
                if isinstance(event, ResponseReceived):
                    print("Response headers:", dict(event.headers))
                elif isinstance(event, DataReceived):
                    print("Response data:", event.data.decode("utf-8"))
                    conn.end_stream(event.stream_id)

            sock.sendall(conn.data_to_send())

run_http2_client("127.0.0.1", int(sys.argv[1]))
