import numpy as np
def run(a: np.ndarray) -> np.ndarray:
    h, w = a.shape
    b = np.zeros((3, 3), dtype=int)
    for y in range(h):
        for x in range(w):
            if a[y, x] == 5:
                b = np.maximum(b, a[y-1:y+2, x-1:x+2])
    return b
