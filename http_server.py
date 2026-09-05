import socket

HOST = "127.0.0.1"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen(5)

print("Server running on port", PORT)

while True:
    client, address = server.accept()

    print("Connected by", address)

    request = client.recv(1024)

    print(request.decode())

    response = """HTTP/1.1 200 OK

<html>
<head><title>Socket Programming</title></head>
<body>
<h1>Hello from Python HTTP Server!</h1>
</body>
</html>
"""

    client.send(response.encode())

    client.close()