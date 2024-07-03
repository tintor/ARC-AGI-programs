import numpy as np
def run(a: np.ndarray):
    h, w = a.shape
    b = np.zeros((h*2, w), dtype=int)
    b[:h, :] = a
    b[h:, :] = np.flipud(a)
    return b
