from math_zxb.sta import C


class BinDistribution:
    def __init__(self, n: int, p_success: float):
        if n <= 0:
            raise ArithmeticError("n must >0")
        if not 0 <= p_success <= 1:
            raise ArithmeticError("p_success must between [0,1]")

        self._n = n
        self._p_success = p_success

    def p(self, x: int):
        if 0 <= x <= self._n:
            return C(self._n, x) * self._p_success ** (x) * (1 - self._p_success) ** (self._n - x)
        else:
            return 0.0

    def cp(self, x: int):
        return sum(self.p(i) for i in range(x + 1))

    @property
    def miu(self):
        return self._n*self._p_success

    @property
    def sigma(self):
        return (self.miu*(1-self._p_success))**0.5


if __name__ == "__main__":
    bd = BinDistribution(5, 0.5)
    print(bd.cp(0))
