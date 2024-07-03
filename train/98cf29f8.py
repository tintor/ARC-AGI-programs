import numpy as np
def get(a: np.ndarray, y: int, x: int) -> int:
    return 0 if y < 0 or x < 0 or y >= a.shape[0] or x >= a.shape[1] else a[y, x]

def is_target(a: np.ndarray, y: int, x: int) -> bool:
    if a[y, x] == 0:
        return False
    cf = 0
    for dy, dx in [(1,0), (-1,0), (0,1), (0,-1)]:
        if get(a, y + dy, x + dx) == a[y, x]:
            cf += 1
    if cf != 1:
        return
    cd = 0
    for dy, dx in [(1,1), (1,-1), (-1,1), (-1,-1)]:
        if get(a, y + dy, x + dx) == a[y, x]:
            cd += 1
    return cd <= 2

def find_target(a: np.ndarray) -> tuple[int, int] | None:
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            if is_target(a, y, x):
                return y, x
    return None

def shift(b: np.ndarray, y: int, x: int):
    h, w = b.shape
    if get(b, y, x + 1) == get(b, y, x):
        # shift left
        b[:, x:w-1] = b[:, x+1:w]
        b[:, w-1] = 0
        return

    if get(b, y, x - 1) == get(b, y, x):
        # shift right
        b[:, 1:x+1] = b[:, 0:x]
        b[:, 0] = 0
        return
        
    if get(b, y + 1, x) == get(b, y, x):
        # shift up
        b[y:h-1, :] = b[y+1:h, :]
        b[h-1, :] = 0
        return

    if get(b, y - 1, x) == get(b, y, x):
        # shift down
        b[1:y+1, :] = b[0:y, :]
        b[0, :] = 0
        return


def run(a: np.ndarray):
    b = a.copy()
    y, x = find_target(a)
    while is_target(b, y, x):
        shift(b, y, x)
    return b
