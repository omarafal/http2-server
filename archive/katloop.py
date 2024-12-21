from hpack import Decoder

# Initialize the HPACK decoder
decoder = Decoder()

def parse_headers_frame(data):
    # Frame header
    length = int.from_bytes(data[:3], byteorder="big")  # 3 bytes
    frame_type = data[3]  # 1 byte
    flags = data[4]  # 1 byte
    stream_id = int.from_bytes(data[5:9], byteorder="big") & 0x7FFFFFFF  # 4 bytes

    print(f"Frame Header:\n  Length: {length}\n  Type: {frame_type}\n  Flags: {flags}\n  Stream ID: {stream_id}")

    if frame_type != 0x01:
        raise ValueError("Expected HEADERS frame, got a different frame type.")

    # Parse the payload
    payload = data[9:9 + length]

    # Handle padding if the PADDED flag is set
    if flags & 0x08:  # PADDED flag
        pad_length = payload[0]
        payload = payload[1:-pad_length]

    # HPACK decode the headers
    decoder = Decoder()
    try:
        headers = decoder.decode(payload)
    except Exception as e:
        print(f"HPACK decoding error: {e}")
        print(f"Problematic payload: {payload}")
        raise
    print("Decoded Headers:")
    for key, value in headers:
        print(f"  {key}: {value}")

    return headers, flags, stream_id


def respond_with_data(tls_socket, stream_id):
    """
    Respond with a DATA frame for the received request.
    """
    # DATA frame header
    response_body = b"Hello, HTTP/2!"
    length = len(response_body).to_bytes(3, byteorder="big")
    frame_type = b"\x00"  # DATA frame type
    flags = b"\x01"  # END_STREAM flag
    stream_id_bytes = stream_id.to_bytes(4, byteorder="big")

    # Construct and send the frame
    frame_header = length + frame_type + flags + stream_id_bytes
    tls_socket.sendall(frame_header + response_body)
    print("Sent DATA frame with response body.")