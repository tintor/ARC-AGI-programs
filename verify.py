import numpy as np
from numpy import ndarray
import traceback
import json
import sys
import os
from utils import run_code_and_verify

color_codes = {
    0: '\033[30m',  # Black
    1: '\033[31m',  # Red
    2: '\033[32m',  # Green
    3: '\033[33m',  # Yellow
    4: '\033[34m',  # Blue
    5: '\033[35m',  # Magenta
    6: '\033[36m',  # Cyan
    7: '\033[37m',  # White
    8: '\033[91m',  #
    9: '\033[92m',  # 
    'reset': '\033[0m'  # Reset to default
}

def print_grid(*grids: ndarray):
    height = max(e.shape[0] for e in grids)
    for y in range(height):
        for i, a in enumerate(grids):
            for x in range(a.shape[1]):
                if y < a.shape[0]:
                    e = a[y, x]
                    color = color_codes.get(e, color_codes['reset'])
                    print(f"{color}{e}", end=' ')
                else:
                    print('  ')

            if i + 1 != len(grids):
                print('  ', end='')
        print(color_codes['reset'])


def list_problems(path: str) -> list[str]:
    return [f[:-5] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.json')]


def load_problem(problem: str) -> tuple[list[tuple[ndarray, ndarray]], list[tuple[ndarray, ndarray]]]:
    doc = None
    for e in ['train', 'eval']:
        f = os.path.join(e, problem + '.json')
        if os.path.isfile(f):
            with open(f, 'r') as file:
                doc = json.load(file)
            break
    assert doc is not None
    train = []
    test = []
    for pair in doc['train']:
        a = np.array(pair['input'], dtype=int)
        b = np.array(pair['output'], dtype=int)
        train.append((a, b))
    for pair in doc['test']:
        a = np.array(pair['input'], dtype=int)
        b = np.array(pair['output'], dtype=int)
        test.append((a, b))
    return train, test



def solve(train: list[ndarray, ndarray], test: list[ndarray], programs: list[str]) -> str:
    out = [None, None]
    for i, program in enumerate(programs):
        ok = True
        for a, b in train:
            c = run_code_and_verify(program, a, out)
            if not isinstance(c, ndarray) or not np.array_equal(b, c):
                ok = False
                break
        if ok:
            for a in test:
                c = run_code_and_verify(program, a, out)
                if not isinstance(c, ndarray):
                    ok = False
                    break
        if ok:
            return program
    return ""


def evaluate(pairs: list[ndarray, ndarray], program: str, debug: bool = False) -> float:
    if program == "":
        print("Failed all cases (no program)")
        return 0.0
    solved = 0
    total = 0
    for a, b in pairs:
        out = ['', '']
        c = run_code_and_verify(program, a, out)
        if debug and len(out[0]) > 0:
            print(out[0])
        if debug and len(out[1]) > 0:
            print(out[1])
        total += 1
        if isinstance(c, ndarray) and np.array_equal(b, c):
            solved += 1
        if debug:
            if isinstance(c, str):
                print_grid(a, b)
                print(f"Failed: {c}")
            elif np.array_equal(b, c):
                print_grid(a, b)
                print("Passed")
            else:
                print_grid(a, b, c)
                print("Failed")
        else:
            print_grid(a, b)
            print()
    return solved / total


if __name__ == "__main__":
    if len(sys.argv) == 2:
        target = sys.argv[1]
        filepath = os.path.join("train", target + ".py")
        with open(filepath, "r") as f:
            program = f.read()

        train, test = load_problem(target)
        score = evaluate(train + test, program, True)
        print("Score {}".format(score))    
        sys.exit(0)

    programs = []
    for name in os.listdir("train"):
        filepath = os.path.join("train", name)
        if os.path.isfile(filepath) and filepath.endswith('.py'):
            with open(filepath, "r") as f:
                programs.append(f.read())

    solved = 0
    total = 0

    for name in list_problems('train'):
        total += 1
        train, test = load_problem(name)
        code = solve(train, [a for a, b in test], programs)
        score = evaluate(train + test, code)
        if score == 1.0:
            solved += 1
            continue
        
        print(name)
        print("Score {}".format(score))
        for a, b in train:
            print("Train")
            print_grid(a, b)
            print()
        for a, b in test:
            print("Test")
            print_grid(a)
            print()
        print()

    print("Solved {}/{} problems".format(solved, total))
