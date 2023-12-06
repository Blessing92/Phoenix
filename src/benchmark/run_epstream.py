import time
import random
import numpy as np

def iterate_func(nr, solve_func, a, b):
    total_time = 0.0
    for _ in range(nr):
        start_time = time.time()
        result = solve_func(a, b)
        end_time = time.time()
        total_time += end_time - start_time
    return result, total_time

def run_epstream(n, nr):
    s = np.random.rand(1)
    a = np.random.rand(n)
    b = np.random.rand(n)
    
    result, t = iterate_func(nr, lambda a, b: s * a + b, a, b)

    data_size_bytes = n * 8 * 2  # Each element is 8 bytes, and there are 2 vectors (a and b)
    num_operations = 2 * n  # Addition and multiplication for each element

    performance = (1e-9) * num_operations * nr / t

    # Convert GB/Sec
    performance_gb_sec = performance * (data_size_bytes / (1024 ** 3))
    
    # Convert MB/Sec
    performance_mb_sec = performance * (data_size_bytes / (1024 ** 2))

    print(f" Performance = {performance_gb_sec} GB/s, {performance_mb_sec} MB/s Total time = {t} sec")

run_epstream(100, 5)
