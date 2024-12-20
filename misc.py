from datetime import datetime
from termcolor import colored
import base64

def b64_decode(msg):
    """
    Decode base64 encoded messages and return it in pure string format
    """
    return str(base64.b64decode(msg.replace("b", "", 1).replace("\'", "", 2))).replace("b", "", 1).replace("\'", "", 2)

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
    print(f"[{datetime.now()}] {data}" if header==None else f"[{datetime.now()}] {colored(header, "red")}\n{data}")


def print_debug(string):
    """
    Format printing for debugging
    """
    print(f"\033[44m{string}\033[0m")