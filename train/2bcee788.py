import numpy as np
from typing import Generator

class int2:
    y: int
    x: int
    __slots__ = ['x', 'y']  # fields are immutable

    def __init__(self, y: int, x: int) -> None:
        self.x = x
        self.y = y
    def __add__(self, o) -> 'int2':
        return int2(self.y + o.y, self.x + o.x)
    def __sub__(self, o) -> 'int2':
        return int2(self.y - o.y, self.x - o.x)
    def __neg__(self) -> 'int2':
        return int2(-self.y, -self.x)
    def tuple(self) -> tuple[int, int]:
        return (self.y, self.x)
    def __iter__(self) -> Generator[int, None, None]:
        yield self.y
        yield self.x
    def __str__(self) -> str:
        return f"{self.y} {self.x}"

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

X = int2(x=1, y=0)
Y = int2(x=0, y=1)

def get(a: np.ndarray, e: int2, default: int = 0) -> int:
    return a[*e] if is_valid(e, a) else default

####################3

def run(a: np.ndarray):
    h, w = a.shape
    for e in indices(a):
        if a[*e] != 2:
            continue

        b = a.copy()
        if get(a, e-Y) not in [0, 2]:
            for i in range(h):
                if e.y + i < h and e.y - i - 1 >= 0:
                    b[e.y + i] = a[e.y - i - 1]
        elif get(a, e+Y) not in [0, 2]:
            for i in range(h):
                if e.y - i >= 0 and e.y + i + 1 < h:
                    b[e.y - i] = a[e.y + i + 1]
        elif get(a, e-X) not in [0, 2]:
            for i in range(w):
                if e.x + i < w and e.x - i - 1 >= 0:
                    b[:, e.x + i] = a[:, e.x - i - 1]
        elif get(a, e+X) not in [0, 2]:
            for i in range(w):
                if e.x - i >= 0 and e.x + i + 1 < w:
                    b[:, e.x - i] = a[:, e.x + i + 1]

        b[np.isin(b, [0])] = 3  # replace all 0s with 3
        return b
