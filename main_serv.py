from misc import *
from constants import *
from datetime import datetime
from push_promise import *


def get_fields(req):
    fields = {}
    for field in req.split("\r\n")[:len(req.split("\r\n")) - 1]:
        try:
            fields[field.split(":")[0]] = field.split(":")[1].strip()
        except:
            pass

    return fields


def ack_settings():
    msg = {
        "length": 0,
        "type": 4,
        "flags": 1,  # For ACK
        "stream-identifier": 0
    }

    send = make_frame(msg)
    return send


def parse_msg(msg):
    """
    Function to return a dictionary form of incoming messages
    """

    sep = msg.strip().split("\r\n")

    di = {}

    for entry in sep:
        temp = entry.split(":")
        di[temp[0].strip()] = temp[1].strip()

    return di


def get_file(path):
    """
    Returns file, status code and possible embedded file paths
    """
    content = ""
    stat = ""
    
    try:

        if not path.startswith("/") or ".." in path:
                with open("./400.html") as file: 
                    content = file.read()
                    stat = f"400 {STATUS[400]}"
                return [content, stat]
        
        if path in FORBIDDEN:
            with open("./403.html") as file:
                content = file.read()
                stat = f"403 {STATUS[403]}"
            return [content, stat]
        
        if path in UNAUTHORIZED:
            with open("./401.html") as file:
                content = file.read()
                stat = f"401 {STATUS[401]}"
            return [content, stat]

        if path in REDIRECTS:
            new_path, permanent = REDIRECTS[path]
            stat = f"{301 if permanent else 302} {STATUS[301 if permanent else 302]}"
            return [f"Redirect to {new_path}", stat]
        
        if path in NO_CONTENT_PATHS:
                stat = f"204 {STATUS[204]}"
                return ["", stat]

        if path == "/":
            path = "/index.html"
    
        path = f".{path}"

        try:
            with open(f"{path}") as file:
                content = file.read()
                stat = f"200 {STATUS[200]}"

        except FileNotFoundError:
            with open("./404.html") as file:
                content = file.read()
                stat = f"404 {STATUS[404]}"

    except Exception as e:
        with open("./500.html") as file:
            content = file.read()
            stat = f"500 {STATUS[500]}"
        print(f"Internal server error: {e}")
    return [content, stat]


# Main flow of program
def main(tls_socket,log):
    # Receive the SETTINGS data
    data = tls_socket.recv(1024)

    # First SETTINGS Frame
    settings = b64_decode(data)
    print_cmd(log,settings, "SETTINGS RECEIVED")

    # ACK on SETTINGS
    send(tls_socket, ack_settings())

    # Await Request
    data = tls_socket.recv(1024)
    request = b64_decode(data)

    print_cmd(log,request, "REQUEST FROM CLIENT")

    # Handle request
    parsed_req = parse_msg(request)
    res_data, res_stat = get_file(parsed_req["path"])

    promise = Promise(tls_socket, res_stat, parsed_req["stream-identifier"], res_data)

    # send promise headers
    try:
        promise.send_headers()
    except PromiseError:
        pass

    # send requested file header

    headerBF = {
        "status": f"{res_stat}",
        "date": f"{datetime.now()}",
    }

    if res_data != "":
        headerBF["content-type"] = "text/html"
        headerBF["content-length"] = f"{len(res_data)}"

    headerBF = make_frame(headerBF)

    header_frame = {
        "length": len(headerBF),
        "type": 1,  # 1 for HEADER frame
        "flags": 4,  # 4 for END_HEADERS
        "stream-identifier": parsed_req["stream-identifier"],
        "header-block-fragment": f"({headerBF})"  # FOR NOW PLAIN TEXT, ENCODE AND MAKE HPACK ON
    }

    send(tls_socket, make_frame(header_frame))

    # send requested file data
    data_frame = {
        "length": len(res_data),
        "type": 0,  # 0 for DATA
        "flags": 1,  # 1 for END_STREAM
        "stream-identifier": parsed_req["stream-identifier"],
        "payload": f"{res_data}",
    }

    send(tls_socket, make_frame(data_frame)) if res_data != "" else None

    # send promise data
    try:
        promise.send_data()
    except PromiseError:
        pass