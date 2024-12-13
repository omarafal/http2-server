from misc import *

def parse_headers(event):
    """
    Parse incoming headers
    RETURNS: parsed_headers
    """
    # Initialize a dictionary to store the parsed headers
    parsed_headers = {}
    
    for key, value in event.headers:
        parsed_headers[key.decode().replace(":", "")] = value.decode()

    return parsed_headers

def handle_request(event):
    """
    Handle requests according to header information
    RETURNS: [response_headers, response_data]
    """
    parsed_req = parse_headers(event)
    # print_debug("THIS RAN")
    # print(parsed_req)
    # init list of headers
    # response_headers = []

    response_data = grab(parsed_req["path"])

    response_headers = [
        (':status', response_data[0]),
        ('content-type', 'text/html'),
    ]

    return [response_headers, response_data]

def grab(path):
    """
    Grab requested data
    RETURNS: [HTTP status code, requested data if exists]
    """

    if path == "/" or path == "/index.html":
        path = "index.html"
    else:
        path = path.replace("/", "")

    try:
        with open(path, "r") as file:
            return ["200 OK", file.read().encode()]
        
    except FileNotFoundError:
        with open("notfound.html", "r") as file:
            return ["404 NOT FOUND", file.read().encode()]