import numpy as np
def run(a: np.ndarray):
    h, w = a.shape
    b = np.zeros((h*2, w*2), dtype=int)
    for y in range(h//2):
        for x in range(w//2):
            p = a[y*2:y*2+2, x*2:x*2+2]
            if np.any(p != 0):
                b[y*4:y*4+4, x*4:x*4+4] = np.max(p)
    return b
