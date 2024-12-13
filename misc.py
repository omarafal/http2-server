from datetime import datetime

def print_cmd(string):
    """
    Format printing
    """
    print(f"[{datetime.now()}] {string}")

def print_debug(string):
    """
    Format printing for debugging
    """
    print(f"\033[44m{string}\033[0m")