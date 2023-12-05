from mpi4py import MPI
import time
import random
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def distribute_work(n, nr, size, rank):
    workload = n // size  # Divide the matrix rows among nodes
    start_row = rank * workload
    end_row = (rank + 1) * workload if rank < size - 1 else n
    return start_row, end_row

def gather_results(results):
    return comm.gather(results, root=0)

def iterate_func(nr, solve_func, a, b):
    total_time = 0.0
    for _ in range(nr):
        start_time = time.time()
        x = solve_func(a, b)
        end_time = time.time()
        total_time += end_time - start_time
    return total_time

def run_hpl_parallel(n, nr, tol=16):
    a = np.random.rand(n, n)
    b = np.random.rand(n, 1)

    start_row, end_row = distribute_work(n, nr, size, rank)
    local_a = a[start_row:end_row, :]
    local_b = b[start_row:end_row, :]

    local_x, local_t = iterate_func(nr, np.linalg.solve, local_a, local_b)
    local_r = np.dot(local_a, local_x) - local_b
    local_r0 = np.linalg.norm(local_r, np.inf)
    local_r1 = local_r0 / (np.finfo(np.float64).eps * np.linalg.norm(local_a, 1) * (end_row - start_row))
    local_r2 = local_r0 / (np.finfo(np.float64).eps * np.linalg.norm(local_a, np.inf) * np.linalg.norm(local_x, np.inf) * (end_row - start_row))
    local_performance = (1e-9 * (2.0 / 3.0 * (end_row - start_row) * n * n + 3.0 / 2.0 * (end_row - start_row) * n) * nr / local_t)
    local_verified = np.max((local_r0, local_r1, local_r2)) < 16

    all_results = gather_results((local_verified, local_performance))

    if rank == 0:
        aggregated_results = np.array(all_results)
        global_verified = all(aggregated_results[:, 0])
        global_performance = np.sum(aggregated_results[:, 1])
        
        if not global_verified:
            raise RuntimeError("Solution did not meet the prescribed tolerance %d" % tol)

        # Convert Gflops to Mflops
        global_performance_mflops = global_performance * 1000
        print(f"{global_performance_mflops} MFlops/Sec, {global_performance} GFlops (Total across all nodes)")

# Example usage:
n = 100
nr = 5
tolerance = 16
run_hpl_parallel(n, nr, tolerance)
