import numpy as np
def run(a: np.ndarray):
    b = a.copy()
    h, w = a.shape
    for y in range(h):
        if np.all(a[y, 1:w-1] == 0):
            b[y, 1:w-1] = 3
    for x in range(w):
        if np.all(a[1:h-1, x] == 0):
            b[1:h-1, x] = 3
    return b        
