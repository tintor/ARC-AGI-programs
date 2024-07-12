import numpy as np

def paint(a: np.ndarray, x: int, y: int, dx: int, dy: int) -> np.ndarray:
    while y >= 0 and x >= 0 and x < a.shape[1] and y < a.shape[0] and a[y, x] != 5:
        a[y, x] = 8
        x += dx
        y += dy

def run(a: np.ndarray) -> np.ndarray:
    h, w = a.shape
    xmin = w
    xmax = 0
    ymin = h
    ymax = 0

    cx = None
    cy = None
    vert = None

    for y in range(1, h-1):
        for x in range(w):
            if a[y, x] == 0 and a[y-1, x] != 0 and a[y+1, x] != 0:
                cx = x
                cy = y
                vert = False
    
    for y in range(h):
        for x in range(1, w-1):
            if a[y, x] == 0 and a[y, x-1] != 0 and a[y, x+1] != 0:
                cx = x
                cy = y
                vert = True
    assert vert is not None

    for y in range(h):
        for x in range(w):
            if a[y, x] != 0:
                xmin = min(xmin, x)
                xmax = max(xmax, x)
                ymin = min(ymin, y)
                ymax = max(ymax, y)

    if vert:
        paint(a, cx, cy, 0, 1)
        paint(a, cx, cy, 0, -1)
    else:
        paint(a, cx, cy, 1, 0)
        paint(a, cx, cy, -1, 0)

    a[ymin+1:ymax, xmin+1:xmax] = 8
    return a
