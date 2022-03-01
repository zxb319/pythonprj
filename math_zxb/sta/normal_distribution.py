import math

from math_zxb import integral


class NormalDistribution:
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


if __name__ == '__main__':
    pd = NormalDistribution(30, 2/6)
    print(pd.cp(28))