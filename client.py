import socket
import ssl
import h2
import hyperframe.frame as hf
from h2.config import H2Configuration
from h2.connection import H2Connection
from h2.events import ResponseReceived, DataReceived
import sys

def run_http2_client(host, port):
    # Create an SSL context for the client
    context = ssl.create_default_context()
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_3
    context.set_alpn_protocols(["h2"])
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE


    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as tls:
            # Ensure HTTP/2 protocol is negotiated
            negotiated_protocol = tls.selected_alpn_protocol()
            if negotiated_protocol != "h2":
                raise RuntimeError("Failed to negotiate HTTP/2. Is the server supporting HTTP/2?")

            # Initialize the HTTP/2 connection
            config = H2Configuration(client_side=True)
            conn = H2Connection(config)
            conn.initiate_connection()
            var = conn.data_to_send()
            tls.sendall(var)
            # print(var)
            rawdata = b'PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n\x00\x00*\x04\x00\x00\x00\x00\x00\x00\x01\x00\x00\x10\x00\x00\x02\x00\x00\x00\x01\x00\x04\x00\x00\xff\xff\x00\x05\x00\x00@\x00\x00\x08\x00\x00\x00\x00\x00\x03\x00\x00\x00d\x00\x06\x00\x01\x00\x00'

            byte_data = memoryview(rawdata)
            print("------------------")
            hf.Frame.explain(byte_data)
            print("------------------")


            # Send an HTTP/2 request
            request_headers = [
                (":method", "GET"),
                (":scheme", "https"),
                (":authority", host),
                (":path", "/for.html"),
            ]
            conn.send_headers(stream_id=1, headers=request_headers, end_stream=False)
            tls.sendall(conn.data_to_send())

            # Receive and process the response
            while True:
                data = tls.recv(65535)
                if not data:
                    break

                events = conn.receive_data(data)
                for event in events:
                    # print(f"EVENT {event}")
                    if isinstance(event, ResponseReceived):
                        print("Response headers:", dict(event.headers))
                    elif isinstance(event, DataReceived):
                        print("Response data:", event.data.decode("utf-8"))

                        # try:
                        conn.end_stream(event.stream_id)
                    

                tls.sendall(conn.data_to_send())
                # conn.close_connection()
                # sock.close()

run_http2_client("127.0.0.1", int(sys.argv[1]))
