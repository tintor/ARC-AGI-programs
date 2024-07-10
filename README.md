Dataset of python solutions of riddles from [ARC-AGI dataset](https://github.com/fchollet/ARC-AGI).

Each solution is a standalone python library containing `def run(a: np.ndarray) -> np.ndarray:` function.

Status:
- Training 12/400
- Evaluation 0/400

Example solution:
```
import numpy as np
def run(a: np.ndarray):
    h, w = a.shape
    b = np.zeros((h*2, w*2), dtype=int)
    for y in range(h//2):
        for x in range(w//2):
            p = a[y*2:y*2+2, x*2:x*2+2]
            if np.any(p != 0):
                b[y*4:y*4+4, x*4:x*4+4] = np.max(p)
    return b
```

Notes:
train/9aec4887.json: all training examples modify only pixels near the edge, but test example also modifies pixesl away from edge
