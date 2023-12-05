import random
import math
from scipy.fft import fft, ifft
from numpy import linalg


def iterate_func(nr, solve_func, a, b):
    total_time = 0.0
    for _ in range(nr):
        start_time = time.time()
        x = solve_func(a, b)
        end_time = time.time()
        total_time += end_time - start_time
    return total_time
    

def run_fft(n, nr, tol=16):
    """
    Run the one-dimensional FFT benchmark on a vector of size n, nr
    number of times and verifies that the inverse transforms recreates
    the original vector up to a tolerance, tol (defaults to 16).
    This function returns the performance in GFlops/sec.
    """
    a = random.rand(n, 1)
    b, t = iterate_func(nr, fft.fft, a)  # Make sure iterate_func is defined
    log2n = math.log(n) / math.log(2)
    performance = 1e-9 * 5.0 * n * log2n * nr / t
    verified = linalg.norm(a - ifft(b)) / (eps * log2n) < tol
    if not verified:
        raise RuntimeError("Solution did not meet the tolerance %d" % tol)
    return performance
