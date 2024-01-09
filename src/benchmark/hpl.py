#hpl.py
import time
import random
import numpy as np


def iterate_func(nr, solve_func, a, b):
    """
    Iterates the solution of the linear system Ax = b using the specified solve_func.

    Parameters:
        nr (int): Number of iterations.
        solve_func (function): Function to solve the linear system.
        a (numpy.ndarray): Coefficient matrix.
        b (numpy.ndarray): Right-hand side vector.

    Returns:
        x (numpy.ndarray): Solution vector.
        total_time (float): Total time taken for all iterations.
    """
    total_time = 0.0
    for _ in range(nr):
        start_time = time.time()
        x = solve_func(a, b)
        end_time = time.time()
        total_time += end_time - start_time

    return x, total_time


def run_hpl(n, nr, tol=16):
    """
    Run the High-performance LINPACK test on a matrix of size n x n, nr
    number of times and ensures that the maximum of the three
    residuals is strictly less than the prescribed tolerance (defaults
    to 16).
    This function returns the performance in GFlops/Sec.
    """
    a = np.random.rand(n, n)
    b = np.random.rand(n, 1)
    print(f"a shape: {a.shape}, b shape: {b.shape}")
    x, t = iterate_func(nr, np.linalg.solve, a, b)
    r = np.dot(a, x) - b
    r0 = np.linalg.norm(r, np.inf)
    r1 = r0 / (np.finfo(np.float64).eps * np.linalg.norm(a, 1) * n)
    r2 = r0 / (np.finfo(np.float64).eps * np.linalg.norm(a, np.inf) * np.linalg.norm(x, np.inf) * n)
    performance = (1e-9 * (2.0 / 3.0 * n * n * n + 3.0 / 2.0 * n * n) * nr / t)
    verified = np.max((r0, r1, r2)) < 16
    if not verified:
        raise RuntimeError("Solution did not meet the prescribed tolerance %d" % tol)

    # Convert Gflops to Mflops
    performance_mflops = performance * 1000
    
    print(f" Performance = {performance_mflops} MFlops/Sec, Total time = {t} sec")


# Example usage:
n = 100
nr = 5
tolerance = 16
run_hpl(n, nr)
