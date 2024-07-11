import numpy as np
def run(a: np.ndarray):
    h, w = a.shape
    for y in range(h - 1, 0, -1):
        for x in range(w):
            if a[y, x] != 2:
                continue
            if a[y - 1, x] == 0:
                a[y - 1, x] = 2
            if a[y - 1, x] == 5 and x < w - 1:
                a[y, x + 1] = 2
    return a
