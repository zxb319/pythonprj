from typing import Callable


def root_binarily(func: Callable[[float], float], lo: float, hi: float):
    if lo > hi:
        raise ArithmeticError("lo<=hi is must.")

    flo = func(lo)
    fhi = func(hi)
    if flo * fhi > 0:
        raise ArithmeticError(f"func(lo)*func(hi)<=0 is must.lo={lo},hi={hi}")

    mi = (lo + hi) / 2
    if mi in (lo, hi):
        return hi

    fmi = func(mi)
    if flo * fmi <= 0:
        return root_binarily(func, lo, mi)
    else:
        return root_binarily(func, mi, hi)


if __name__ == '__main__':
    f = lambda x: x- 2
    print(root_binarily(f, 0, 3))
    print(2 ** (1 / 3))
