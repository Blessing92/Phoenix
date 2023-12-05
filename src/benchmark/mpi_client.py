from mpi4py import MPI
import socket
import time
import random
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Server-client socket communication
def perform_computation_with_server(data):
    try:
        # Connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('<laptop_ip>', 8080)  # Replace with the IP address of your laptop
        client_socket.connect(server_address)

        # Receive data from the server
        received_data = client_socket.recv(1024).decode()
        start_row, end_row = map(int, received_data.split(','))

        # Perform local computation
        a = np.random.rand(end_row - start_row, 100)
        b = np.random.rand(end_row - start_row, 1)
        x = np.linalg.solve(a, b)
        r = np.dot(a, x) - b
        r0 = np.linalg.norm(r, np.inf)
        r1 = r0 / (np.finfo(np.float64).eps * np.linalg.norm(a, 1) * (end_row - start_row))
        r2 = r0 / (np.finfo(np.float64).eps * np.linalg.norm(a, np.inf) * np.linalg.norm(x, np.inf) * (end_row - start_row))
        performance = (1e-9 * (2.0 / 3.0 * (end_row - start_row) * 100 * 100 + 3.0 / 2.0 * (end_row - start_row) * 100) * 5 / 1)
        verified = np.max((r0, r1, r2)) < 16

        # Send the result back to the server
        client_socket.send(np.array([performance]).tobytes())

        # Close the connection
        client_socket.close()

    except Exception as e:
        print(f"Error in client (rank {rank}): {e}")

# Example usage
perform_computation_with_server("100,5,16")
