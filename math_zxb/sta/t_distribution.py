import math

import math_zxb
from math_zxb.sta.distributions import Dist


class TDistribution(Dist):
    def __init__(self, k: int):
        self._k = k

        def f(x: float):
            a = math.gamma((k + 1) / 2) * (1 + x ** 2 / k) ** (-(k + 1) / 2)
            b = (k * math.pi) ** 0.5 * math.gamma(k / 2)

            return a / b

        self._pdf = f

    def cp(self, x: float):
        lo = min(0, x)
        hi = max(0, x)
        res = math_zxb.integral(self._pdf, lo, hi)
        if x < 0:
            return 0.5 - res
        else:
            return 0.5 + res

    def pbetween(self, lo: float, hi: float):
        assert lo <= hi
        return math_zxb.integral(self._pdf, lo, hi)

    def x_of(self,p:float):
        assert 0<p<1
        return math_zxb.root_binarily(lambda x:self.cp(x)-p,-100,100)

    def range_of(self, p: float):
        assert 0 < p < 1

        def f(x: float):
            return math_zxb.integral(self._pdf, -x, x) - p

        res = math_zxb.root_binarily(f, -100, 100)
        return -res, res
