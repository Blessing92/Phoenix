import socket

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server address and port
server_address = ('<Machine 1 IP>', 12345)  # Replace with the actual IP of Machine 1

# Connect to the server
client_socket.connect(server_address)

# Input the operands (e.g., 1 and 1)
operand1 = "1"
operand2 = "1"

# Send the first operand
client_socket.send(operand1.encode())

# Receive the result for the first operand
result1 = client_socket.recv(1024).decode()
print(f"Result for {operand1}: {result1}")

# Send the second operand
client_socket.send(operand2.encode())

# Receive the result for the second operand
result2 = client_socket.recv(1024).decode()
print(f"Result for {operand2}: {result2}")

# Close the socket
client_socket.close()
