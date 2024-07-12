import numpy as np
def run(a: np.ndarray) -> np.ndarray:
    a[0:3, 4:7] = np.rot90(a[0:3, 0:3], -1)
    a[0:3, 8:11] = np.rot90(a[0:3, 0:3], -2)
    return a
