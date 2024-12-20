# -*- coding: utf-8 -*-
"""
http2_server_sync.py
~~~~~~~~~~~~~~~~~~~~

A basic HTTP/2 server implemented without asyncio. Uses threads for handling
connections. Requires Python 3.5+ and the hyper-h2 library.
"""
import socket
import ssl
import threading
import io
import collections
from typing import List, Tuple

from h2.config import H2Configuration
from h2.connection import H2Connection
from h2.events import (
    ConnectionTerminated, DataReceived, RequestReceived,
    StreamEnded, StreamReset, WindowUpdated
)
from h2.errors import ErrorCodes
from h2.exceptions import ProtocolError, StreamClosedError

RequestData = collections.namedtuple('RequestData', ['headers', 'data'])

class H2ThreadedServer:
    def __init__(self, host: str, port: int, certfile: str, keyfile: str):
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile

    def start(self):
        # Create SSL context
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_COMPRESSION
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        context.set_alpn_protocols(["h2"])

        # Create socket and wrap with SSL
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(5)
        print(f"Serving on {self.host}:{self.port}")

        while True:
            conn, addr = sock.accept()
            conn = context.wrap_socket(conn, server_side=True)
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

    def handle_client(self, conn, addr):
        print(f"Connection from {addr}")
        protocol = H2ThreadedProtocol(conn)
        protocol.run()
        conn.close()


class H2ThreadedProtocol:
    def __init__(self, transport):
        self.conn = H2Connection(config=H2Configuration(client_side=False, header_encoding='utf-8'))
        self.transport = transport
        self.stream_data = {}

    def run(self):
        try:
            self.conn.initiate_connection()
            self.transport.sendall(self.conn.data_to_send())

            while True:
                data = self.transport.recv(65535)
                if not data:
                    break

                events = self.conn.receive_data(data)
                self.transport.sendall(self.conn.data_to_send())

                for event in events:
                    if isinstance(event, RequestReceived):
                        self.request_received(event.headers, event.stream_id)
                    elif isinstance(event, DataReceived):
                        self.receive_data(event.data, event.stream_id)
                    elif isinstance(event, StreamEnded):
                        self.stream_complete(event.stream_id)
                    elif isinstance(event, StreamReset):
                        self.stream_reset(event.stream_id)
        except (ProtocolError, ConnectionResetError):
            pass

    def request_received(self, headers: List[Tuple[str, str]], stream_id: int):
        headers = collections.OrderedDict(headers)
        self.stream_data[stream_id] = RequestData(headers, io.BytesIO())

    def receive_data(self, data: bytes, stream_id: int):
        stream_data = self.stream_data.get(stream_id)
        if stream_data:
            stream_data.data.write(data)

    def stream_complete(self, stream_id: int):
        request_data = self.stream_data.pop(stream_id, None)
        if not request_data:
            return

        response_body = b"<html><body><h1>Hello, HTTP/2!</h1></body></html>"
        response_headers = (
            (':status', '200'),
            ('content-type', 'text/html'),
            ('content-length', str(len(response_body))),
            ('server', 'h2-threaded-server'),
        )

        self.conn.send_headers(stream_id, response_headers)
        self.conn.send_data(stream_id, response_body, end_stream=True)
        self.transport.sendall(self.conn.data_to_send())

    def stream_reset(self, stream_id):
        pass


if __name__ == "__main__":
    server = H2ThreadedServer(host="127.0.0.1", port=8443, certfile="server.crt", keyfile="server.key")
    try:
        server.start()
    except KeyboardInterrupt:
        print("Server shutting down.")
