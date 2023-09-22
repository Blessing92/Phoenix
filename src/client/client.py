import socket

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server address and port
server_address = ('<Machine 1 IP>', 12345)  # Replace with the actual IP of Machine 1

# Connect to the server
client_socket.connect(server_address)

# Input a number for which you want to calculate the factorial
number = 10  # You can change this to any positive integer

# Send the number to the server
client_socket.send(str(number).encode())

# Receive the result from the server
result = client_socket.recv(1024).decode()
print(f"Result for {number}!: {result}")

# Close the socket
client_socket.close()
