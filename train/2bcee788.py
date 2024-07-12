import numpy as np
def run(a: np.ndarray):
    h, w = a.shape
    for y in range(h):
        for x in range(w):
            if a[y, x] == 2:
                return flip(a, y, x)

def flip(a: np.ndarray, y: int, x: int):
    h, w = a.shape
    b = a.copy()

    if y > 0 and a[y - 1, x] != 0 and a[y - 1, x] != 2:
        # flip down
        for i in range(h):
            if y + i < h and y - i - 1 >= 0:
                b[y + i] = a[y - i - 1]

    if y < h-1 and a[y + 1, x] != 0 and a[y + 1, x] != 2:
        # flip up
        for i in range(h):
            if y - i >= 0 and y + i + 1 < h:
                b[y - i] = a[y + i + 1]
    
    if x > 0 and a[y, x - 1] != 0 and a[y, x - 1] != 2:
        for i in range(w):
            if x + i < w and x - i - 1 >= 0:
                b[x + i] = a[x - i - 1]

    if x < w-1 and a[y, x + 1] != 0 and a[y, x + 1] != 2:
        for i in range(w):
            if x - i >= 0 and x + i + 1 < w:
                b[x - i] = a[x + i + 1]

    for y in range(h):
        for x in range(w):
            if b[y, x] in [2, 0]:
                b[y, x] = 3
    return b
