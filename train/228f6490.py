import numpy as np
def equal_shapes(a: list, b: list) -> bool:
    if len(a) != len(b):
        return False
    delta = np.array(a[0]) - np.array(b[0])
    for p, q in zip(a, b):
        if not np.array_equal(np.array(p) - np.array(q), delta):
            return False
    return True

def try_move_item_to_hole(b: np.ndarray, holes: list, items: list) -> bool:
    for q in items:
        for p in holes:
            if equal_shapes(p[3], q[3]):
                for y, x in p[3]:
                    b[y, x] = q[0]
                for y, x in q[3]:
                    b[y, x] = 0
                holes.remove(p)
                items.remove(q)
                return True
    return False

def all_monocolor_shapes(a: np.ndarray) -> list[tuple[int, tuple, tuple, list[tuple]]]:
    shapes = []
    visited = np.zeros(a.shape, dtype=int)
    h, w = a.shape
    for y in range(h):
        for x in range(w):
            if visited[y, x] != 0:
                continue
            count = 0
            maxc = minc = (y, x)
            queue = []
            pixels = []

            def add(yy, xx):
                nonlocal queue, count, maxc, minc, visited
                if yy < 0 or xx < 0 or yy >= h or xx >= w or visited[yy, xx] == 1 or a[yy, xx] != a[y, x]:
                    return
                visited[yy, xx] = 1
                queue.append((yy, xx))
                pixels.append((yy, xx))
                count += 1
                minc = (min(yy, minc[0]), min(xx, minc[1]))
                maxc = (max(yy, maxc[0]), max(xx, maxc[1]))

            add(y, x)
            while len(queue) > 0:
                yy, xx = queue.pop(0)
                add(yy - 1, xx)
                add(yy + 1, xx)
                add(yy, xx - 1)
                add(yy, xx + 1)

            ww = maxc[1] - minc[1] + 1
            hh = maxc[0] - minc[0] + 1
            norm_shape = np.zeros((hh, ww), dtype=int)
            for yy, xx in pixels:
                norm_shape[yy - minc[0], xx - minc[1]] = 1

            pixels.sort()
            shapes.append((a[y, x], minc, maxc, pixels))
    return shapes

def run(a: np.ndarray):
    b = a.copy()
    shapes = all_monocolor_shapes(b)
    holes = [e for e in shapes if e[0] == 0]
    items = [e for e in shapes if e[0] != 0]
    items.sort(key = lambda e: e[0])

    my_items = []
    for i, q in enumerate(items):
        prev_color = items[i - 1][0] if i > 0 else 0
        next_color = items[i + 1][0] if i + 1 < len(items) else 0
        if q[0] != prev_color and q[0] != next_color:
            my_items.append(q)

    while try_move_item_to_hole(b, holes, my_items):
        pass
    return b
