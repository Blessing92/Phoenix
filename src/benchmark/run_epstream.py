
import time
import random

def iterate_func(nr, solve_func, a, b):
    total_time = 0.0
    for _ in range(nr):
        start_time = time.time()
        x = solve_func(a, b)
        end_time = time.time()
        total_time += end_time - start_time
    return total_time


def run_epstream(n, nr):
    """
    Run the embarrassingly parallel stream benchmark on vectors of size
    n, nr number of times.
    This function returns the performance of the benchmark in
    GFlops/second.
    """
    s = random.rand(1)
    a = random.rand(n)
    b = random.rand(n)
    c, t = iterate_func(nr, lambda s, a, b: s * a + b, s, a, b)
    performance = (1e-9) * 24.0 * nr * n / t
    return performance
