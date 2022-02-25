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
    pd = NormalDistribution(0, 1)

    from math_zxb import root_binarily

    a = root_binarily(lambda x: pd.cp(x) - 0.0110, -100, 100)
    print(a)

    pd = NormalDistribution(10, 2)
    print(pd.pbetween(11, 13.6))

    pd = NormalDistribution(38.5, 2.5)
    print(1 - pd.pbetween(36, 40))
