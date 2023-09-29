import socket
import math

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('192.168.8.100', 8080)  # Use any available port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print("Server is ready to receive connections...")

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    # Receive data from the client (expecting a positive integer)
    data = client_socket.recv(1024).decode()

    try:
        # Perform the computation (calculate the factorial)
        number = int(data)
        if number < 0:
            raise ValueError("Factorial is defined for non-negative integers.")
        result = math.factorial(number)
        print(f"Received: {data}, Result: {result}")
        client_socket.send(str(result).encode())
    except ValueError as e:
        print(f"Invalid input received from client: {e}")
    except OverflowError:
        print("Factorial result is too large to send to the client.")

    # Close the client socket
    client_socket.close()
