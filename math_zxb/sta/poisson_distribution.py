import math

from math_zxb.sta import A


class PoissonDistribution:
    def __init__(self, _lambda: float):
        if _lambda <= 0:
            raise ArithmeticError("lambda must >0")
        self._lambda = _lambda

    def p(self, x: int):
        if x < 0:
            raise ArithmeticError("x must >=0")
        return self._lambda ** x * math.e ** (-self._lambda) / A(x, x)

    @property
    def miu(self):
        return self._lambda

    @property
    def sigma(self):
        return self._lambda ** 0.5


if __name__ == '__main__':
    pd = PoissonDistribution(0.05 * 20)
    print(pd.p(2))
