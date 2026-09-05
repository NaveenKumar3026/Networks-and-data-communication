import socket
import os

HOST = "127.0.0.1"
PORT = 8888

proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy.bind((HOST, PORT))
proxy.listen(5)

print("Proxy Server Running...")

while True:

    client, addr = proxy.accept()

    request = client.recv(4096).decode()

    if not request:
        client.close()
        continue

    try:
        first_line = request.split("\n")[0]
        url = first_line.split()[1]

        filename = url.replace("/", "_")

        if os.path.exists(filename):

            print("Cache Hit")

            with open(filename, "rb") as file:
                client.send(file.read())

        else:

            print("Cache Miss")

            host = url.split("/")[2]

            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect((host,80))

            server.send(request.encode())

            response = b""

            while True:
                data = server.recv(4096)
                if not data:
                    break
                response += data

            with open(filename,"wb") as file:
                file.write(response)

            client.send(response)

            server.close()

    except Exception as e:
        print(e)

    client.close()









    