import numpy as np
def run(a: np.ndarray) -> np.ndarray:
    p = np.amax(a)
    h, w = a.shape
    for y in range(h):
        c = 0
        for x in range(w):
            a[y, x] = c + 1
            c = (c + y) % p
    return a
