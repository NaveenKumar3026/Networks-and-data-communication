import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080

# Create UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind socket to IP address and port
server.bind((SERVER_IP, SERVER_PORT))

print("UDP HTTP Server is running...")
print("Waiting for client request...")

while True:

    # Receive request
    data, client_address = server.recvfrom(4096)

    request = data.decode()

    print("Request received:")
    print(request)

    # Web page content
    webpage = """
<!DOCTYPE html>
<html>
<head>
    <title>UDP HTTP Server</title>
</head>
<body>
    <h1>Hello from UDP Web Server!</h1>
    <p>This web page was downloaded using a UDP socket.</p>
</body>
</html>
"""

    # Send webpage to client
    server.sendto(webpage.encode(), client_address)

    # Send end marker
    server.sendto(b"END", client_address)

    print("Web page sent to client.")