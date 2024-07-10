import numpy as np
def run(a: np.ndarray) -> np.ndarray:
    h, w = a.shape

    src_xmin = w
    src_ymin = h
    src_xmax = 0
    src_ymax = 0

    dest_xmin = w
    dest_ymin = h
    dest_xmax = 0
    dest_ymax = 0

    for y in range(h):
        for x in range(w):
            if a[y, x] not in [0, 8]:
                dest_xmin = min(dest_xmin, x)
                dest_xmax = max(dest_xmax, x)
                dest_ymin = min(dest_ymin, y)
                dest_ymax = max(dest_ymax, y)
            if a[y, x] == 8:
                src_xmin = min(src_xmin, x)
                src_xmax = max(src_xmax, x)
                src_ymin = min(src_ymin, y)
                src_ymax = max(src_ymax, y)

    src_w = src_xmax - src_xmin + 1
    src_h = src_ymax - src_ymin + 1

    dest_w = dest_xmax - dest_xmin + 1
    dest_h = dest_ymax - dest_ymin + 1

    assert src_w + 2 == dest_w
    assert src_h + 2 == dest_h

    b = a[dest_ymin:dest_ymax+1, dest_xmin:dest_xmax+1]
    b[1:-1, 1:-1] = a[src_ymin:src_ymax+1, src_xmin:src_xmax+1]

    for y in range(1, dest_h-1):
        for x in range(1, dest_w-1):
            e = b[y, x]
            if e == 0:
                continue

            up = y
            down = dest_h - 1 - y
            left = x
            right = dest_w - 1 - x

            if up < min(left, right):
                b[y, x] = b[0, x]
            if left < min(up, down):
                b[y, x] = b[y, 0]
            if down < min(left, right):
                b[y, x] = b[-1, x]
            if right < min(up, down):
                b[y, x] = b[y, -1]

    return b
