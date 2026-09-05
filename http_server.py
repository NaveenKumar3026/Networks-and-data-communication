import socket

HOST = "127.0.0.1"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"HTTP Server listening on http://{HOST}:{PORT}")

while True:
    client_socket, address = server_socket.accept()

    request = client_socket.recv(1024).decode()

    print("\n========== HTTP REQUEST ==========")
    print(request)

    html = """
    <html>
        <body>
            <h1>Welcome to HTTP Server</h1>
            <h2>Networks and Data Communication</h2>
        </body>
    </html>
    """

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(html)}\r\n"
        "Connection: close\r\n\r\n"
        + html
    )

    client_socket.sendall(response.encode())
    client_socket.close()