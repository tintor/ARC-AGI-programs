import numpy as np
def run(a: np.ndarray):
    b = a.copy()
    h, w = a.shape
    for y in range(h):
        s = None
        for x in range(w):
            if a[y, x] == 0:
                continue
            if s is not None:
                if a[y, s] == a[y, x]:
                    b[y, s:x] = a[y, x]
            s = x
    return b
