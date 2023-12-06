from mpi4py import MPI
import socket
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def distribute_work(n, nr, size):
    workload = n // size
    start_rows = [rank * workload for rank in range(size)]
    end_rows = [(rank + 1) * workload if rank < size - 1 else n for rank in range(size)]
    return start_rows, end_rows

def gather_results(results):
    return comm.gather(results, root=0)

# Server-client socket communication
def perform_computation_with_clients(data):
    try:
        # Connect to the clients
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('192.168.1.75', 8080)  # Use 0.0.0.0 to listen on all available interfaces
        server_socket.bind(server_address)
        server_socket.listen(size)  # Number of expected clients

        print(f"Server (rank {rank}) is ready to receive connections...")

        # start_rows, end_rows = distribute_work(*map(int, data.split(',')), size)
        print(f"size: {size}")
        start_rows, end_rows = distribute_work(*map(int, data.split(',')), size=size)

        connected_clients = 0 
        print(f"Number of connected clients: {connected_clients}")

        # Wait until the specified number of clients are connected
        while connected_clients < 4:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from client (rank {connected_clients + 1})")

            # Send data to the client
            client_socket.send(f"{start_rows[connected_clients + 1]},{end_rows[connected_clients + 1]}".encode())

            # Close the client socket
            client_socket.close()

            connected_clients += 1

        # Collect results from clients
        all_results = [np.empty((0,)) for _ in range(size)]
        for client_rank in range(1, size):
            client_socket, _ = server_socket.accept()
            result = np.frombuffer(client_socket.recv(1024), dtype=np.float64)
            all_results[client_rank] = result

            # Close the client socket
            client_socket.close()

        # Perform final aggregation on the server (rank 0)
        if rank == 0:
            aggregated_results = np.concatenate(all_results)
            global_performance = np.sum(aggregated_results)

            # Convert Gflops to Mflops
            global_performance_mflops = global_performance * 1000
            print(f"{global_performance_mflops} MFlops/Sec, {global_performance} GFlops (Total across all clients)")

    except Exception as e:
        print(f"Error in server: {e}")

# Example usage
if rank == 0:
    print(f"server rank: {rank}")
    perform_computation_with_clients("100,5,16")
