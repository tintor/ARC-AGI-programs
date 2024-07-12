import numpy as np
from numpy import ndarray
import json
import signal
from contextlib import contextmanager
import io as io___
import sys as sys___
import traceback


def run_code_and_verify(code: str, in_matrix: ndarray, out: list[str] | None) -> ndarray | str:
    max_duration = 60
    try:
        with time_limit(max_duration):
            result = run_code(code, np.copy(in_matrix), out)
    except TimeoutException:
        return "Your solution timed out after {} seconds.".format(max_duration)
    except Exception as e:
        return "{}\n{}".format(e, traceback.format_exc())
    if not isinstance(result, ndarray) or len(result.shape) != 2:
        return "Your output must be a 2d matrix of type ndarray."
    if np.any(result < 0) or np.any(result > 9):
        return "Your output matrix contains numbers out of [0, 9] range."
    return result


def run_code(code: str, arg: ndarray, out: list[str] | None) -> ndarray:
    if out is not None:
        sys___.stdout = io___.StringIO()
        sys___.stderr = io___.StringIO()
        sys___.stdout.close = lambda *args, **kwargs: None
        sys___.stderr.close = lambda *args, **kwargs: None

    globals_before__ = globals().copy()
    try:
        exec(code, globals(), globals())
        result = run(arg)
    finally:
        #globals().clear()
        globals().update(globals_before__)
        for k in set(globals().keys()) - globals_before__.keys():
            del globals()[k]

        if out is not None:
            out[0] = sys___.stdout.getvalue()
            out[1] = sys___.stderr.getvalue()

            sys___.stdout = sys___.__stdout__
            sys___.stderr = sys___.__stderr__
    return result


class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
