from mpi4py import MPI
import time
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def update_state(ran, idx, table_size):
    # Generate random values on rank 0 and broadcast to all processes
    if rank == 0:
        ran = np.random.rand(len(ran))  # Replace this with your actual random value generation logic
    comm.Bcast(ran, root=0)

    # Scatter indices among processes
    scattered_idx = np.zeros_like(idx)
    comm.Scatter([idx, MPI.INT], [scattered_idx, MPI.INT], root=0)

    # Perform your update logic here using the received ran and scattered_idx
    # For example, you might update a subset of a larger table with the random values
    # t[scattered_idx] ^= ran

    # Gather the updated indices back to the root process
    gathered_idx = np.zeros_like(idx)
    comm.Gather([scattered_idx, MPI.INT], [gathered_idx, MPI.INT], root=0)

    if rank == 0:
        # Combine the updated indices from all processes
        # Implement your aggregation logic here if needed
        updated_indices = gathered_idx
    else:
        updated_indices = None

    # Broadcast the combined result to all processes
    updated_indices = comm.bcast(updated_indices, root=0)

    # Update the original idx array with the combined result
    idx[:] = updated_indices

def update(table_size, n_in, n_out):
    t1 = 0
    t0 = time.time()
    t = np.arange(table_size)
    t1 += (time.time() - t0)
    ran = np.zeros(n_in)
    idx = np.arange(n_in)

    for outer in range(int(n_out)):
        update_state(ran, idx, table_size)
        t0 = time.time()
        t[idx] = t[idx] ^ ran.astype(int)  # Convert ran to integers before XOR
        t1 += (time.time() - t0)
    return n_in * n_out / t1

def run_random_access(n, nr):
    n_in = 1024
    n_out = nr / n_in
    if n_out * n_in != nr:
        raise ValueError("Number of updates must be evenly divisible by %d" % n_in)
    return update(n, n_in, n_out)

def main():
    n = 1024  # Set your desired value for n
    nr = 1024 * 1024  # Set your desired value for nr

    local_nr = nr // size
    local_result = run_random_access(n, local_nr)

    global_result = comm.reduce(local_result, op=MPI.SUM, root=0)

    if rank == 0:
        # Convert the result to GigaUpdates per Second (GUPs)
        global_result_gups = global_result / 1e9
        print(f"Performance: {global_result_gups} GUPs")

if __name__ == "__main__":
    main()
