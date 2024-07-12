import numpy as np
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
    h, w = a.shape
    b = None
    b_size = h * w
    for color, minc, maxc, pixels in all_monocolor_shapes(a):
        ww = maxc[1] - minc[1] + 1
        hh = maxc[0] - minc[0] + 1
        if len(pixels) == hh * ww and len(pixels) < b_size:
            b_size = len(pixels)
            b = a[minc[0]:maxc[0]+1, minc[1]:maxc[1]+1]
    return b
