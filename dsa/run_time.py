import time
from typing import Callable
import functools


def run_time(c: Callable):
    """打印出可执行对象的执行时间"""

    @functools.wraps(c)
    def inner(*args, **kwargs):
        start_time = time.time()
        res = c(*args, **kwargs)
        print(f"{c}的执行时间:{time.time() - start_time}s,args({args},{kwargs})")
        return res

    return inner


class CostTime:
    """用with代码块打印代码块的执行时间"""

    def __enter__(self):
        print(rf'代码块开始执行...')
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(rf'代码块的执行时间：{time.time() - self.start_time}s')


if __name__ == '__main__':
    # @run_time
    def ttt():
        return sum(i for i in range(10 ** 8))

    with CostTime():
        print(ttt())
