import ssl
import socket
from misc import *
import hpack_own

stream_id = 0
# path = sys.argv[1]
port = 8443

def pri_make():
    """
    Preface function for settings
    """
    req = {
        "magic": "PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n",
        "length": 24,
        "type": 4,
        "flags": 0,
        "stream-identifier": f"{stream_id}",
        "SETTINGS": "SETTINGS_MAX_FRAME_SIZE=16384 SETTINGS_ENABLE_PUSH=1",
    }

    send = make_frame(req)

    return send

def alpn_client(path,log):
    # Create a socket
    client_socket = socket.create_connection(('localhost', int(port)))

    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cafile="certs/ca.crt")
    context.set_alpn_protocols(["h2", "http/1.1"])

    # Wrap the socket with SSL
    with context.wrap_socket(client_socket, server_hostname="localhost") as tls_socket:
        selected_protocol = tls_socket.selected_alpn_protocol()
        print_cmd(log,selected_protocol, f"ALPN Protocol Negotiated")

        # Send PRI Frame and SETTINGS
        pri = pri_make()
        send(tls_socket, pri)

        # Await ACK From Server
        data = b64_decode(tls_socket.recv(1024))
        print_cmd(log,data, "ACK ON SETTINGS")

        # Request File
        HTTP_REQUEST = {
            "method" : "GET",
            "path": f"{path}",
            "host": "localhost",
            "stream-identifier": stream_id+1 if stream_id == 0 else stream_id+2,
        }

        client_req = make_frame(HTTP_REQUEST)

        HEADER_REQUEST = {
            "length": len(client_req),
            "type": 4,
            "flags": 0,
            "stream-identifier": f"{stream_id}",
            "header-block-fragment": f"{hpack_own.encode(HTTP_REQUEST)}",
        }

        send(tls_socket, make_frame(HEADER_REQUEST))

        # Await Server Response
        data = "s" # init data dummy for while (lol)
        while data:
            data = b64_decode(tls_socket.recv(1024))
            print_cmd(log,data, "SERVER RESPONSE") if data != "" else None

            if "header-block-fragment" in data:
                data = parse_msg(data)

                data_l = list(str(data["header-block-fragment"]))
                data_l.pop()
                data_l.pop(0)
                data_l.pop(0)

                data = "".join(data_l)

                bytes_data = bytes(data, 'utf-8').decode('unicode_escape').encode('latin1')
                print_cmd(log, f"{str(hpack_own.decode(bytes_data))}\n", "DECODED HEADER BLOCK")


