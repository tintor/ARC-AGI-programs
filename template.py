import numpy as np
from typing import Generator

class int2:
    y: int
    x: int
    __slots__ = ['x', 'y']  # fields are immutable

    def __init__(self, y: int, x: int) -> None:
        self.x = x
        self.y = y
    def __add__(self, o) -> int2:
        return int2(self.x + o.x, self.y + o.y)
    def __sub__(self, o) -> int2:
        return int2(self.x - o.x, self.y - o.y)
    def tuple(self) -> tuple[int, int]:
        return (self.y, self.x)
    def __iter__(self) -> Generator[int, None, None]:
        yield self.y
        yield self.x

def is_valid(v: int2, a: np.ndarray) -> bool:
    h, w = a.shape
    return v.x >= 0 and v.y >= 0 and v.x < w and v.y < h

def indices(a: np.ndarray) -> Generator[int2, None, None]:
    assert len(a.shape) == 2
    h, w = a.shape
    for y in range(h):
        for x in range(w):
            yield int2(y, x)

def vmin(a: int2, b: int2) -> int2:
    return int2(min(a.y, b.y), min(a.x, b.x))

def vmax(a: int2, b: int2) -> int2:
    return int2(max(a.y, b.y), max(a.x, b.x))

X = int2(x=1, y=1)
Y = int2(x=0, y=1)

def all_monocolor_shapes(a: np.ndarray) -> list[tuple[int, int2, int2, list[int2]]]:
    shapes = []
    visited = np.zeros(a.shape, dtype=int)
    for e in indices(a):
        if visited[*e] != 0:
            continue
        maxc = minc = e
        queue = []
        pixels = []

        def add(v):
            nonlocal queue, maxc, minc, visited
            if not is_valid(v, a) or visited[*v] == 1 or a[*v] != a[*e]:
                return
            visited[*v] = 1
            queue.append(v)
            pixels.append(v)
            minc = vmin(minc, v)
            maxc = vmax(maxc, v)

        add(e)
        while len(queue) > 0:
            q = queue.pop(0)
            add(q - Y)
            add(q + Y)
            add(q - X)
            add(q + X)

        norm_shape = np.zeros((maxc - minc + X + Y).tuple(), dtype=int)
        for p in pixels:
            norm_shape[*(p - minc)] = 1

        pixels.sort()
        shapes.append((a[*e], minc, maxc, pixels))
    return shapes

def run(a: np.ndarray) -> np.ndarray:
    return a
