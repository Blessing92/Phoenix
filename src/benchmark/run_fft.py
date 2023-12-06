import random
import math
import time  # Add this import
import numpy as np
from scipy.fft import fft, ifft
from numpy import linalg

eps = np.finfo(float).eps  # Define eps

def iterate_func(nr, solve_func, a):
    total_time = 0.0
    for _ in range(nr):
        start_time = time.time()
        x = solve_func(a)
        end_time = time.time()
        total_time += end_time - start_time
    return x, total_time  # Return the result x as well

def run_fft(n, nr, tol=16):
    """
    Run the one-dimensional FFT benchmark on a vector of size n, nr
    number of times and verifies that the inverse transforms recreates
    the original vector up to a tolerance, tol (defaults to 16).
    This function returns the performance in GFlops/sec.
    """
    a = np.random.rand(n, 1)
    b, t = iterate_func(nr, fft, a)
    log2n = math.log(n) / math.log(2)
    performance = 1e-9 * 5.0 * n * log2n * nr / t
    verified = linalg.norm(a - ifft(b)) / (eps * log2n) < tol
    if not verified:
        raise RuntimeError("Solution did not meet the tolerance %d" % tol)
    
    # Convert Gflops to Mflops
    performance_mflops = performance * 1000
    print(f" Performance = {performance_mflops} MFlops/Sec, Total time = {t} sec")

run_fft(100, 5)
