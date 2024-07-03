import numpy as np
def run(a: np.ndarray):
    b = a.copy()
    h, w = a.shape
    for y in range(h):
        for x in range(w):
            p = a[max(0,y-1):min(h,y+2), max(0,x-1):min(h,x+2)]
            if np.all(p == 0):
                b[y, x] = 3

    done = False
    while not done:
        done = True
        for y in range(h):
            for x in range(w):
                if is_corner(b, y, x):
                    b[y, x] = 0
                    done = False
    return b

def count3s(b: np.ndarray, y: int, x: int, dy: int, dx: int) -> bool:
    c = 1
    while True:
        y += dy
        x += dx
        if y < 0 or x < 0 or y >= b.shape[0] or x >= b.shape[1] or b[y, x] != 3:
            return c
        c += 1

def until_edge3s(b: np.ndarray, y: int, x: int, dy: int, dx: int) -> bool:
    while True:
        y += dy
        x += dx
        if y < 0 or x < 0 or y >= b.shape[0] or x >= b.shape[1]:
            return True
        if b[y, x] != 3:
            return False

def is_corner(b: np.ndarray, y: int, x: int) -> bool:
    if b[y, x] != 3:
        return False
    u = b[y-1, x] if y > 0 else 3
    d = b[y+1, x] if y + 1 < b.shape[0] else 3
    l = b[y, x-1] if x > 0 else 3
    r = b[y, x+1] if x + 1 < b.shape[1] else 3
    s = f"{u}{l}{d}{r}"
    if s in ["0000", "3000", "0300", "0030", "0003"]:
        return True
    if s in ["3300", "0330", "0033", "3003"]:
        if u and count3s(b, y, x, -1, 0) <= 6:
            return True
        if l and count3s(b, y, x, 0, -1) <= 6:
            return True
        if d and count3s(b, y, x, 1, 0) <= 6:
            return True
        if r and count3s(b, y, x, 0, 1) <= 6:
            return True

        n = 0
        if u and until_edge3s(b, y, x, -1, 0):
            n += 1
        if l and until_edge3s(b, y, x, 0, -1):
            n += 1
        if d and until_edge3s(b, y, x, 1, 0):
            n += 1
        if r and until_edge3s(b, y, x, 0, 1):
            n += 1

        return n == 0
    return False
