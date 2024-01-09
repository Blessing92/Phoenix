import subprocess
import time

# Number of clients
num_clients = 4

# Command to run the client script
client_command = "python mpi_client.py"

# Start multiple client processes
processes = []

for i in range(num_clients):
    process = subprocess.Popen(client_command, shell=True)
    processes.append(process)
    time.sleep(1)  # Add a delay to stagger the start of each client

# Wait for all processes to finish
for process in processes:
    process.wait()

print("All clients have completed.")
