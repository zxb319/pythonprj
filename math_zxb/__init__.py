from typing import Callable


def differential(f: Callable[[float], float], x: float):
    delta = 0.0000001
    return (f(x + delta) - f(x)) / delta


def integral(func: Callable[[float], float], lo: float, hi: float):
    n = 1_0000
    delta = (hi - lo) / n
    res = 0
    for i in range(n):
        res += (func(lo + delta * (i)) + func(lo + delta * (i + 1))) / 2 * delta

    return res


def root_binarily(func: Callable[[float], float], lo: float, hi: float):
    if lo > hi:
        raise ArithmeticError("lo<=hi is must.")

    flo = func(lo)
    fhi = func(hi)
    if flo * fhi > 0:
        print(lo,flo,hi,fhi)
        raise ArithmeticError(f"func(lo)*func(hi)<=0 is must.lo={lo},hi={hi}")

    while True:
        mi = (lo + hi) / 2
        if mi in (lo, hi):
            return hi

        fmi = func(mi)
        if flo * fmi <= 0:
            hi = mi
        else:
            lo = mi
            flo = fmi


if __name__ == '__main__':
    a=1