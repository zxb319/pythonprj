import math

import math_zxb
from math_zxb.sta.distributions import Dist


class KaiDistribution(Dist):
    """K*S**2/sigma**2服从该分布"""

    def __init__(self, k: int):
        self._k = k

        def f(x: float):
            a = x ** (k / 2 - 1) * math.e ** (-x / 2)
            b = 2 ** (k / 2) * math.gamma(k / 2)
            return a / b

        self._pdf = f

    def cp(self, x: float):
        assert x >= 0
        return math_zxb.integral(self._pdf, 0, x)

    def pbetween(self, lo: float, hi: float):
        assert lo <= hi
        return math_zxb.integral(self._pdf, lo, hi)

    def x_of(self, p: float):
        assert 0 < p < 1
        return math_zxb.root_binarily(lambda x: self.cp(x) - p, 0, 100)

    def range_of(self, p: float):
        assert 0 < p < 1

        lo = math_zxb.root_binarily(lambda x: self.cp(x) - (1 - p) / 2, 0, 100)
        hi = math_zxb.root_binarily(lambda x: self.cp(x) - (1 + p) / 2, 0, 100)

        return lo, hi


if __name__ == '__main__':
    pd = KaiDistribution(9)
    p = pd.cp(9 * 0.0025 / 0.001)
    print(1 - p)
