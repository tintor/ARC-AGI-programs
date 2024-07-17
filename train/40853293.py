import numpy as np
from typing import Generator, Callable

class int2:
    y: int
    x: int
    __slots__ = ['x', 'y']  # fields are immutable

    def __init__(self, y: int, x: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, o: 'int2') -> 'int2':
        return int2(self.y + o.y, self.x + o.x)
    def __sub__(self, o: 'int2') -> 'int2':
        return int2(self.y - o.y, self.x - o.x)
    def __neg__(self) -> 'int2':
        return int2(-self.y, -self.x)
    def __mul__(self, a: int) -> 'int2':
        return int2(self.y * a, self.x * a)
    def __floordiv__(self, a: int) -> 'int2':
        return int2(self.y // a, self.x // a)

    def tuple(self) -> tuple[int, int]:
        return (self.y, self.x)
    def __iter__(self) -> Generator[int, None, None]:
        yield self.y
        yield self.x

    def __repr__(self) -> str:
        return f"{self.y} {self.x}"
    def __str__(self) -> str:
        return f"{self.y} {self.x}"

    def __eq__(self, o: object) -> bool:
        return isinstance(o, int2) and self.y == o.y and self.x == o.x
    def __ne__(self, o: object) -> bool:
        return not (self == o)

    def __lt__(self, o: 'int2') -> bool:
        return self.y < o.y or (self.y == o.y and self.x < o.x)
    def __ge__(self, o: 'int2') -> bool:
        return not (self < o)

    def __le__(self, o: 'int2') -> bool:
        return self.y < o.y or (self.y == o.y and self.x <= o.x)
    def __gt__(self, o: 'int2') -> bool:
        return not (self <= o)

def is_valid(v: int2, a: np.ndarray) -> bool:
    h, w = a.shape
    return v.x >= 0 and v.y >= 0 and v.x < w and v.y < h

def indices(a: np.ndarray) -> Generator[int2, None, None]:
    assert len(a.shape) == 2
    h, w = a.shape
    for y in range(h):
        for x in range(w):
            yield int2(y, x)

def vmin(*a: int2) -> int2:
    assert len(a) > 0
    x = y = 0
    for e in a:
        x = min(x, e.x)
        y = min(y, e.y)
    return int2(x=x, y=y)

def vmax(*a: int2) -> int2:
    assert len(a) > 0
    x = y = 0
    for e in a:
        x = max(x, e.x)
        y = max(y, e.y)
    return int2(x=x, y=y)

X = int2(x=1, y=0)
Y = int2(x=0, y=1)

def bfs(a: np.ndarray, start: int2, diagonal: bool, allow: Callable[[int], bool], visited: np.ndarray | None = None) -> list[int2]:
    if visited is None:
        visited = np.full(a.shape, False, dtype=bool)
    queue = []

    def add(v):
        nonlocal queue, visited
        if not is_valid(v, a) or visited[*v] or not allow(a[*v]):
            return
        visited[*v] = True
        queue.append(v)

    pixels = []
    add(start)
    while len(queue) > 0:
        q = queue.pop(0)
        add(q - Y)
        add(q + Y)
        add(q - X)
        add(q + X)
        if diagonal:
            add(q + X + Y)
            add(q + X - Y)
            add(q - X + Y)
            add(q - X - Y)
        pixels.append(q)

    pixels.sort()
    return pixels

def all_monocolor_shapes(a: np.ndarray) -> list[tuple[int, int2, int2, list[int2]]]:
    shapes = []
    visited = np.full(a.shape, False, dtype=bool)
    for e in indices(a):
        if visited[*e]:
            continue
        pixels = bfs(a, e, diagonal=False, allow=lambda c: c == a[*e], visited=visited)

        minc = maxc = e
        for o in pixels:
            minc = vmin(minc, o)
            maxc = vmax(maxc, o)

        pixels.sort()
        shapes.append((a[*e], minc, maxc, pixels))
    return shapes

def all_fg_shapes(a: np.ndarray, bg: list[int]) -> list[tuple[int, int2, int2, list[int2]]]:
    shapes = []
    visited = np.full(a.shape, False, dtype=bool)
    for e in indices(a):
        if a[*e] in bg:
            continue
        pixels = bfs(a, e, diagonal=False, allow=lambda c: c not in bg, visited=visited)

        minc = maxc = e
        for o in pixels:
            minc = vmin(minc, o)
            maxc = vmax(maxc, o)

        pixels.sort()
        shapes.append((a[*e], minc, maxc, pixels))
    return shapes

#################

def run(a: np.ndarray) -> np.ndarray:
    digits = []
    for i in range(10):
        digits.append([])

    for e in indices(a):
        c = a[*e]
        if c != 0:
            digits[c].append(e)

    for c, d in enumerate(digits):
        if len(d) != 2:
            continue
        if d[0].y == d[1].y:
            for x in range(min(d[0].x, d[1].x) + 1, max(d[0].x, d[1].x)):
                a[d[0].y, x] = c

    for c, d in enumerate(digits):
        if len(d) != 2:
            continue
        if d[0].x == d[1].x:
            for y in range(min(d[0].y, d[1].y) + 1, max(d[0].y, d[1].y)):
                a[y, d[0].x] = c

    return a
