import numpy as np
def run(a: np.ndarray):
    b = np.zeros((3, 3), dtype=int)
    for y in range(3):
        for x in range(3):
            b[y, x] = 6 if a[y, x] != 0 or a[y, x + 3] != 0 else 0
    return b        
