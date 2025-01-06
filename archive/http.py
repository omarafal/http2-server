import socket

HOST = '127.0.0.1'  # localhost
PORT = 8443         # Port to listen on

# Read the content of the index.html file
try:
    with open("index.html", "r") as file:
        html_content = file.read()
except FileNotFoundError:
    print("index.html not found in the current directory.")
    exit(1)

# Define the HTTP response
response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: {len(html_content)}

{html_content}"""

# Create and configure the socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)  # Listen for 1 connection at a time
    print(f"Serving HTTP on {HOST} port {PORT} (http://{HOST}:{PORT}/) ...")

    while True:
        # Accept a connection
        client_socket, client_address = server_socket.accept()
        with client_socket:
            print(f"Connection from {client_address}")
            request = client_socket.recv(1024).decode("utf-8")
            print(f"Request:\n{request}")
            
            # Respond with the index.html content
            client_socket.sendall(response.encode("utf-8"))
