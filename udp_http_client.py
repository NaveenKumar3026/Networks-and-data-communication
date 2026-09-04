import socket

# Server details
SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080

# Create UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# HTTP GET request
request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"

# Send request to server
client.sendto(request.encode(), (SERVER_IP, SERVER_PORT))

# Receive response
response = b""

while True:
    try:
        data, server_address = client.recvfrom(4096)

        if not data:
            break

        response += data

        # Server indicates end of transmission
        if b"END" in data:
            break

    except socket.timeout:
        break

# Close socket
client.close()

# Remove END marker
response = response.replace(b"END", b"")

# Save webpage
with open("downloaded_page.html", "wb") as file:
    file.write(response)

print("Web page downloaded successfully!")
print("Saved as downloaded_page.html")