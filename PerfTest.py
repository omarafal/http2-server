import ssl
import socket
from misc import *
import sys
import threading
import time

stream_id = 0
path = sys.argv[1]

# Metrics
latency_times = []
lock = threading.Lock()  # For thread-safe operations on shared metrics


def pri_make():
    """
    Preface function for settings
    """
    req = {
        "Magic": "PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n",
        "Length": 24,
        "Type": 4,
        "Flags": 0,
        "Stream Identifier": f"{stream_id}",
        "SETTINGS": "Max Frame Size = 16384",
    }

    send = make_frame(req)

    return send


def alpn_client():
    """
    Function to send a single request to the server using ALPN
    """
    global stream_id
    start_time = time.time()  # Start timing the request

    try:
        # Create a socket
        client_socket = socket.create_connection(('localhost', 8443))

        # Create SSL context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(cafile="certs/ca.crt")
        context.set_alpn_protocols(["h2", "http/1.1"])

        # Wrap the socket with SSL
        with context.wrap_socket(client_socket, server_hostname="localhost") as tls_socket:
            selected_protocol = tls_socket.selected_alpn_protocol()
            print_cmd(selected_protocol, f"ALPN Protocol Negotiated")

            # Send PRI Frame and SETTINGS
            pri = pri_make()
            send(tls_socket, pri)

            # Await ACK From Server
            data = b64_decode(tls_socket.recv(1024))
            print_cmd(data, "ACK ON SETTINGS")

            # Request File
            HTTP_REQUEST = {
                "method": "GET",
                "path": f"/{path}",
                "host": "localhost",
                "stream-identifier": stream_id + 1 if stream_id == 0 else stream_id + 2,
            }

            send(tls_socket, make_frame(HTTP_REQUEST))

            # Await Server Response
            data = "s"  # init data dummy for while (lol)
            while data:
                data = b64_decode(tls_socket.recv(1024))
                print_cmd(data, "SERVER RESPONSE") if data != "" else None

    except Exception as e:
        print_cmd(str(e), "Error")

    finally:
        # Record latency
        end_time = time.time()
        latency = end_time - start_time
        with lock:
            latency_times.append(latency)


# Measure total execution time
total_start_time = time.time()

# Run the client to make 10 requests
threads = []
for _ in range(10000):
    t = threading.Thread(target=alpn_client)
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

total_end_time = time.time()
total_duration = total_end_time - total_start_time

# Calculate aggregated metrics
average_latency = sum(latency_times) / len(latency_times) if latency_times else 0
min_latency = min(latency_times) if latency_times else 0
max_latency = max(latency_times) if latency_times else 0

# Print metrics
print_cmd(f"Completed 10k requests in {total_duration:.4f} seconds", "INFO")
print_cmd(f"Average Latency: {average_latency:.4f} seconds", "METRICS")
print_cmd(f"Minimum Latency: {min_latency:.4f} seconds", "METRICS")
print_cmd(f"Maximum Latency: {max_latency:.4f} seconds", "METRICS")
