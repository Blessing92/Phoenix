import socket

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server address and port
server_address = ('192.168.8.116', 8080)

# Connect to the server
print("connecting to the server ....")
try:
    client_socket.connect(server_address)
    print("Connected to the server!")
except Exception as e:
    print("Connection failed ", str(e))
    raise


# Input a number for which you want to calculate the factorial
number = 4  # You can change this to any positive integer

# Send the number to the server
client_socket.send(str(number).encode())

# Receive the result from the server
result = client_socket.recv(1024).decode()
print(f"Result for {number}!: {result}")

# Close the socket
client_socket.close()
