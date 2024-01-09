# Server code
from mpi4py import MPI
import socket
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
num_clients = 4

def distribute_work(n, nr, size):
    workload = n // size
    start_rows = [r * workload for r in range(size)]
    end_rows = [(r + 1) * workload if r < size - 1 else n for r in range(size)]
    return start_rows, end_rows

# Server-client socket communication
def perform_computation_with_clients(data):
    try:
        # Connect to the clients
        print(f"connecting to client...")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Print and broadcast the server address to all processes
        server_address = ('192.168.1.75', 8000)  # Use a unique port for each rank
        print(f"Server address: {server_address}")
        server_address_bytes = str(server_address).encode()

        # Broadcast the server address to all processes
        server_address_bytes = comm.bcast(server_address_bytes, root=0)

        server_socket.bind(server_address)
        server_socket.listen(num_clients)

        print(f"Server (rank {rank}) is ready to receive connections...")
        start_rows, end_rows = distribute_work(*map(int, data.split(',')), num_clients)

        connected_clients = 0
        all_results = [np.empty((0,)) for _ in range(num_clients)]

        # Generate random matrices on the server
        a = np.random.rand(int(data.split(',')[0]), int(data.split(',')[0]))
        b = np.random.rand(int(data.split(',')[0]), 1)

        # Wait until the specified number of clients are connected
        while connected_clients < num_clients:
            client_socket, _ = server_socket.accept()
            print(f"Connection from client (rank {connected_clients + 1})")

            # Send data (matrices) to the client
            client_socket.send((a, b).tobytes())

            # Collect results from the client
            result = np.frombuffer(client_socket.recv(1024), dtype=np.float64)
            print(f"Results from client (rank {connected_clients + 1}): {result}")
            all_results[connected_clients] = result

            # Close the client socket
            client_socket.close()

            connected_clients += 1

        print(f"All clients have completed.")

        # Perform final aggregation on the server (rank 0)
        aggregated_results = comm.gather(np.concatenate(all_results), root=0)

        if rank == 0:
            global_performance = np.sum(aggregated_results)
            # Convert Gflops to Mflops
            global_performance_mflops = global_performance * 1000 / (25 * 100 * num_clients)
            print(f"All results: {aggregated_results}")
            print(f"{global_performance_mflops} MFlops/Sec, {global_performance} GFlops (Total across all clients)")

    except Exception as e:
        print(f"Error in server: {e}")



print(f"Server (rank {rank}) calling perform_computation_with_clients")
# Example usage
perform_computation_with_clients("100,5")
