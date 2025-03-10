import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))  # آدرس و پورت سرور
server_socket.listen(1)

print("Server is listening for incoming connections...")
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

while True:
    print("Next Signal ...\n")
    message = client_socket.recv(1024)
    if not message:
        break
    print(f"Received message: {message.decode('utf-8')}")