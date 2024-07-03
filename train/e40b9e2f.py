import numpy as np
def run(a: np.ndarray):
    a = a.copy()
    h, w = a.shape

    cx = None
    cy = None
    cs = None

    # find core 2x2 or 3x3
    for y in range(h - 2):
        for x in range(w - 2):
            if is_symmetrical_non_black(a[y:y+3, x:x+3]):
                assert cs is None
                cx = x
                cy = y
                cs = 3
    if cs is None:
        for y in range(h - 1):
            for x in range(w - 1):
                if is_symmetrical_non_black(a[y:y+2, x:x+2]):
                    assert cs is None
                    cx = x
                    cy = y
                    cs = 2   
    assert cs is not None

    dl = cx
    dr = w - cs - cx
    left = max(0, dr - dl)
    right = max(0, dl - dr)

    du = cy
    dd = h - cs - cy
    up = max(0, dd - du)
    down = max(0, du - dd)

    while left + w + right > up + h + down:
        up += 1
        down += 1
    while left + w + right < up + h + down:
        left += 1
        right += 1
    assert left + w + right == up + h + down

    # expand grid with zeros so that core is exactly in center
    if left > 0:
        a = np.append(np.zeros((h, left), dtype=int), a, axis = 1)
        h, w = a.shape
    if right > 0:
        a = np.append(a, np.zeros((h, right), dtype=int), axis = 1)
        h, w = a.shape
    if up > 0:
        a = np.append(np.zeros((up, w), dtype=int), a, axis = 0)
        h, w = a.shape
    if down > 0:
        a = np.append(a, np.zeros((down, w), dtype=int), axis = 0)
        h, w = a.shape

    # rotate grid 4 times and combine
    a = _max(a, np.flipud(np.transpose(a)))
    a = _max(a, np.fliplr(np.transpose(a)))
    a = _max(a, np.fliplr(np.flipud(a)))

    # undo expansions
    while left > 0:
        a = np.delete(a, (0), axis=1)
        left -= 1
    while right > 0:
        a = np.delete(a, (a.shape[1] - 1), axis=1)
        right -= 1
    while up > 0:
        a = np.delete(a, (0), axis=0)
        up -= 1
    while down > 0:
        a = np.delete(a, (a.shape[0] - 1), axis=0)
        down -= 1

    return a


def _max(a,b):
    c = a.copy()
    h, w = a.shape
    for y in range(h):
        for x in range(w):
            c[y, x] = max(a[y, x], b[y, x])
    return c


def is_symmetrical_non_black(b: np.ndarray):
    return np.all(b != 0) and np.array_equal(b, np.transpose(b)) and np.array_equal(b, np.flipud(b)) and np.array_equal(b, np.fliplr(b))
