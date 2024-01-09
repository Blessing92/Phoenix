# Client code
import os
import time
import socket
import random
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Function to establish a connection and perform communication
def communicate_with_server(rank):
    # Create a new socket for each rank
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Receive the server address and port from the server
    server_address_bytes = comm.bcast(None, root=0)
    
    print(f"Client (rank {rank}) Received server_address_bytes: {server_address_bytes}")

    # Check if server_address_bytes is not None before attempting to decode
    if server_address_bytes is not None:
        server_address = eval(server_address_bytes.decode())

        try:
            print(f"Client (rank {rank}) Successfully connected to server!")
            print(f"Client (rank {rank}) Server address: {server_address}")
            print(f"Client (rank {rank}) Waiting for data from the server...")

            # Connect to the server using the received address
            client_socket.connect(server_address)

            # Receive data (matrices) from the server
            received_data = client_socket.recv(4096)  # Adjust the buffer size as needed
            a, b = np.frombuffer(received_data, dtype=np.float64).reshape(-1, 1)

            # Perform local computation
            x = np.linalg.solve(a, b)
            r = np.dot(a, x) - b
            r0 = np.linalg.norm(r, np.inf)
            r1 = r0 / (np.finfo(np.float64).eps * np.linalg.norm(a, 1) * len(b))
            r2 = r0 / (np.finfo(np.float64).eps * np.linalg.norm(a, np.inf) * np.linalg.norm(x, np.inf) * len(b))
            performance = (1e-9 * (2.0 / 3.0 * len(b) * len(b) * len(b) + 3.0 / 2.0 * len(b) * len(b)) * 5 / 1)
            verified = np.max((r0, r1, r2))

            # Send the result back to the server
            client_socket.send(np.array([performance]).tobytes())

        except Exception as e:
            print(f"Client (rank {rank}) Error: {e}")

        finally:
            # Close the connection
            client_socket.close()
    else:
        print(f"Client (rank {rank}) Error: Received None for server_address_bytes")


# Call the function for each rank
communicate_with_server(rank)
