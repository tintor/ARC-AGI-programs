import numpy as np

def dfs(a: np.ndarray, y: int, x: int):
    h, w = a.shape

    near = []
    if x > 0:
        near.append((y, x-1))
    if x + 1 < w:
        near.append((y, x+1))
    if y > 0:
        near.append((y-1, x))
    if y + 1 < h:
        near.append((y+1, x))

    b = 0
    for e in near:
        if a[*e] not in [0, 8]:
            b = a[*e]

    for e in near:
        if a[*e] == 0:
            a[*e] = b
            dfs(a, e[0], e[1])

def run(a: np.ndarray) -> np.ndarray:
    c = np.where((a != 0) & (a != 8))
    for y, x in zip(c[0], c[1]):
        dfs(a, y, x)
    return a
