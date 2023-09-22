import socket

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('0.0.0.0', 12345)  # Use any available port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print("Server is ready to receive connections...")

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    # Receive data from the client
    data = client_socket.recv(1024).decode()

    # Perform the addition operation
    operands = data.split("+")
    if len(operands) == 2:
        result = int(operands[0]) + int(operands[1])
        print(f"Received: {data}, Result: {result}")
        client_socket.send(str(result).encode())

    # Close the client socket
    client_socket.close()
