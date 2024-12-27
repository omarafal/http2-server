from datetime import datetime
from termcolor import colored
import base64

def send(tls_socket, msg):
    tls_socket.sendall(base64.b64encode(msg.encode("utf-8")))

def b64_encode(msg):
    return base64.b64encode(msg.encode("utf-8"))

def b64_decode(msg):
    """
    Decode base64 encoded messages and return it in pure string format
    """
    return str(base64.b64decode(msg).decode("utf-8"))

def make_frame(header):
    """
    Function to create request from dictionaries provided
    """
    frame = ""
    for key, value in header.items():
        frame += f"{key}: {value}\r\n"

    return frame

def print_cmd(data, header=None):
    """
    Format printing
    """
    print(f"[{datetime.now()}] {data}" if header==None else (f"[{datetime.now()}] {colored(header, "red")}{"\n" if len(data) > 6 else ": "}{data}"))

def print_debug(string):
    """
    Format printing for debugging
    """
    print(f"\033[44m{string}\033[0m")