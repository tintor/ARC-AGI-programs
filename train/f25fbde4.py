import numpy as np
def run(a: np.ndarray) -> np.ndarray:
    h, w = a.shape
    xmin = w
    xmax = 0
    ymin = h
    ymax = 0
    for y in range(h):
        for x in range(w):
            if a[y, x] == 4:
                xmin = min(xmin, x)
                xmax = max(xmax, x)
                ymin = min(ymin, y)
                ymax = max(ymax, y)

    b = a[ymin:ymax+1, xmin:xmax+1]
    return np.kron(b, np.ones((2, 2)))
