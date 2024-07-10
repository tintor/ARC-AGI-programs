import numpy as np
def run(a: np.ndarray) -> np.ndarray:
    h, w = a.shape

    bh = a.copy()
    ch = 0
    for y in range(h):
        unique, counts = np.unique(bh[y], return_counts=True)
        i = np.argmax(counts)
        ch += w - counts[i]
        bh[y] = unique[i]

    bv = a.copy()
    cv = 0
    for x in range(w):
        unique, counts = np.unique(bv[:, x], return_counts=True)
        i = np.argmax(counts)
        cv += h - counts[i]
        bv[:, x] = unique[i]

    return bh if ch < cv else bv
