import numpy as np
def run(a: np.ndarray):
    h, w = a.shape
    return a[:, :w//2] if w % 2 == 0 and np.array_equal(a[:, :w//2], a[:, w//2:]) else a[:h//2, :]
