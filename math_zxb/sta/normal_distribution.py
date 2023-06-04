import math

import math_zxb
from math_zxb import integral
from math_zxb.sta.distributions import Dist


class NormalDistribution(Dist):
    def __init__(self, miu: float, sigma: float):
        self._miu = miu
        self._sigma = sigma

        def func(x: float):
            return 1 / (2 * math.pi) ** 0.5 / self._sigma * math.e ** (-(x - self._miu) ** 2 / 2 / self._sigma ** 2)

        self._df = func

    def cp(self, x: float):
        lo = min(self._miu, x)
        hi = max(self._miu, x)

        a = integral(self._df, lo, hi)

        if x < self._miu:
            return 0.5 - a
        else:
            return 0.5 + a

    def pbetween(self, lo: float, hi: float):
        return integral(self._df, lo, hi)

    def x_of(self, p: float):
        assert 0 < p < 1

        return math_zxb.root_binarily(lambda x: self.cp(x) - p, self._miu - 100 * self._sigma, self._miu + 100 * self._sigma)

    def range_of(self, p: float = 0.95):
        assert 0 < p < 1

        def f(x: float):
            return self.pbetween(self._miu - x, self._miu + x) - p

        res = math_zxb.root_binarily(f, self._miu - 100 * self._sigma, self._miu + 100 * self._sigma)
        return self._miu - res, self._miu + res

    def miu(self):
        return self._miu

    def sigma(self):
        return self._sigma


if __name__ == '__main__':
    pd = NormalDistribution(0, 1)
    print(pd.x_of(0.95))
