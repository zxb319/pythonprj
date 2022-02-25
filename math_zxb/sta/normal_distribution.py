import math

from math_zxb import integral


class NormalDistribution:
    def __init__(self, miu: float, sigma: float):
        self._miu = miu
        self._sigma = sigma

    def cp(self, x: float):
        lo = min(self._miu, x)
        hi = max(self._miu, x)

        def func(x: float):
            return 1 / (2 * math.pi) ** 0.5 / self._sigma * math.e ** (-(x - self._miu) ** 2 / 2 / self._sigma ** 2)

        a = integral(func, lo, hi)

        if x < self._miu:
            return 0.5 - a
        else:
            return 0.5 + a


if __name__ == '__main__':
    pd = NormalDistribution(0,1)
    print(pd.cp(1.96)-pd.cp(0))
    print(pd.cp(1.81)-pd.cp(-1.81))
    print(pd.cp(2.42)-pd.cp(0.53))
    print(1-pd.cp(-0.36))
