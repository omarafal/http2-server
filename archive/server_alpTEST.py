import socket
import ssl
from archive.katloop import *

def parse_settings_frame(data):
    """
    Parse the SETTINGS frame from the received HTTP/2 data.
    """
    # Connection preface validation
    preface = data[:24].decode("utf-8")
    if preface != "PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n":
        raise ValueError("Invalid HTTP/2 preface")
    print("Connection preface is valid.")

    # Parse the frame header (9 bytes)
    frame_header = data[24:33]
    length = int.from_bytes(frame_header[:3], byteorder="big")
    frame_type = frame_header[3]
    flags = frame_header[4]
    stream_id = int.from_bytes(frame_header[5:9], byteorder="big") & 0x7FFFFFFF  # Mask reserved bit

    print(f"Frame Header:\n  Length: {length}\n  Type: {frame_type}\n  Flags: {flags}\n  Stream ID: {stream_id}")

    # Ensure it's a SETTINGS frame (type 0x04)
    if frame_type != 0x04:
        raise ValueError("Expected SETTINGS frame, received different frame type.")

    # Parse the SETTINGS frame payload (length specified in the frame header)
    payload = data[33:33 + length]
    settings = []
    for i in range(0, len(payload), 6):  # Each setting is 6 bytes
        identifier = int.from_bytes(payload[i:i + 2], byteorder="big")
        value = int.from_bytes(payload[i + 2:i + 6], byteorder="big")
        settings.append((identifier, value))
    
    print("Parsed SETTINGS Frame:")
    for setting in settings:
        identifier, value = setting
        print(f"  Identifier: {identifier}, Value: {value}")
    
    return settings


def send_settings_ack(tls_socket):
    """
    Send a SETTINGS frame acknowledgment to the client.
    """
    frame_header = (
        b"\x00\x00\x00"  # Length: 0 (no payload for ACK)
        b"\x04"          # Type: SETTINGS
        b"\x01"          # Flags: ACK (0x1)
        b"\x00\x00\x00\x00"  # Stream ID: 0 (connection-level frame)
    )
    tls_socket.sendall(frame_header)
    print("Sent SETTINGS ACK frame.")


def main(tls_socket):
    # Receive the request data
    data = tls_socket.recv(1024)
    print("Received data:", data)

    # Parse the SETTINGS frame
    settings = parse_settings_frame(data)

    # Send SETTINGS frame ACK
    send_settings_ack(tls_socket)

    data = tls_socket.recv(1024)
    print("ACK on settings:", data)


    data = tls_socket.recv(1024)
    print("Header: ", data)
    # Parse the HEADERS frame
    headers, flags, stream_id = parse_headers_frame(data)

    print(headers)

    # Respond with DATA frame if END_STREAM flag is set
    if flags & 0x01:  # END_STREAM
        respond_with_data(tls_socket, stream_id)


# ALPN server
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
        print(f"Connection from {address}")
        try:
            with context.wrap_socket(client_socket, server_side=True) as tls_socket:
                selected_protocol = tls_socket.selected_alpn_protocol()
                print(f"ALPN Protocol Negotiated: {selected_protocol}")

                # Call the main function to handle incoming data
                main(tls_socket)

        except ssl.SSLError as e:
            print(f"SSL Error: {e}")
        finally:
            client_socket.close()


alpn()

# Received data: b"\x00\x01\x1b\x01%\x00\x00\x00\x03\x00\x00\x00\x00)\x82\x04\x81cA\x8a\xa0\xe4\x1d\x13\x9d\t\xb8\xf3M3\x87z\xbc\xd0\x7ff\xa2\x81\xb0\xda\xe0S\xfa\xe4j\xa4?\x84)\xa7z\x81\x02\xe0\xfbS\x91\xaaq\xaf\xb5<\xb8\xd7\xda\x96w\xb8\x16Y\\\x1f\xda\x98\x8aN\xa7`@\x08\x00\x10\x05L&\xb0\xb2\x9f\xcb\x01e\x95\xc1S\xb0I|\xa5\x89\xd3M\x1fC\xae\xba\x0cA\xa4\xc7\xa9\x8f3\xa6\x9a?\xdf\x9ah\xfa\x1du\xd0b\r&=Ly\xa6\x8f\xbe\xd0\x01w\xfe\xbeX\xf9\xfb\xed\x00\x17{Q\x8b-Kp\xdd\xf4Z\xbe\xfb@\x05\xdbP\x92\x9b\xd9\xab\xfaRB\xcb@\xd2_\xa5#\xb3\xe9OhL\x9f@\x92\xb6\xb9\xac\x1c\x85X\xd5 \xa4\xb6\xc2\xada{ZT%\x1f\x81\x0f@\x8aAH\xb4\xa5I'ZB\xa1?\x86\x90\xe4\xb6\x92\xd4\x9f@\x8aAH\xb4\xa5I'Z\x93\xc8_\x86\xa8}\xcd0\xd2_@\x8aAH\xb4\xa5I'Y\x06I\x7f\x83\xa8\xf5\x17@\x8aAH\xb4\xa5I'Z\xd4\x16\xcf\x82\xff\x03@\x86\xae\xc3\x1e\xc3'\xd7\x85\xb6\x00}(o@\x82I\x7f\x86M\x835\x05\xb1\x1f\x00\x00\x04\x08\x00\x00\x00\x00\x03\x00\xbe\x00\x00"