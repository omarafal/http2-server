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
    RETURNS: response_headers
    """
    parsed_req = parse_headers(event)

    response_headers = [
        (':status', '200'),
        ('content-type', 'text/html'),
    ]

    # init list of headers
    # response_headers = []

    # for key, val in parsed_req:
    #     if key == "method":
    #         if val == "GET":
    #             pass
    #     if key == "path":
    #         pass
    #     pass

    return response_headers