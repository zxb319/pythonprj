import time
from typing import Callable
import functools


def run_time(c: Callable):
    @functools.wraps(c)
    def inner(*args, **kwargs):
        start_time = time.time()
        res = c(*args, **kwargs)
        print(f"{c}的执行时间:{time.time() - start_time}s")
        return res

    return inner


if __name__ == '__main__':
    @run_time
    def ttt():
        sum(1 for i in range(10**8))
        return 1


    ttt()
