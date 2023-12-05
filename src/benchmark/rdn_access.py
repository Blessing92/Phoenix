import time
import starp as sp

def update_state(ran, idx, table_size):
    sp.runCommand('rng_update_state', ran, idx, table_size)

def update(table_size, n_in, n_out):
    t1 = 0
    t0 = time.time()
    t = sp.arange(table_size)
    t1 += (time.time() - t0)
    ran = sp.zeros(n_in)
    idx = sp.zeros(n_in)
    for outer in range(int(n_out)):
        update_state(ran, idx, table_size)
        t0 = time.time()
        t[idx] ^= ran
        t1 += (time.time() - t0)
    return 1.0e-9 * n_in * n_out / float(t1)

def run_random_access(n, nr):
    n_in = 1024
    n_out = nr / n_in
    if n_out * n_in != nr:
        raise ValueError("Number of updates must be evenly divisible by %d" % n_in)
    return update(n, n_in, n_out)
