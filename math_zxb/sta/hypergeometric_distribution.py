from dsa.fraction import Fraction
from math_zxb.sta import C


class HypergeometricDistribution:
    def __init__(self, n: int, m: int, a: int):
        """
        n:总数
        m:感兴趣的个数
        a:抽取的总个数
        """
        if m < 0 or n <= 0 or n < m or a < 0 or a > n:
            raise ArithmeticError("m must >=0 and n must >0 and 0<=a<=n")

        self._n = n
        self._m = m
        self._a = a

    def p(self, x: int):
        if x < 0 or x > self._a:
            raise ArithmeticError(f"x must between [0,{self._a}]")

        if x<=self._m:
            return C(self._m, x) * C(self._n - self._m, self._a - x)/C(self._n, self._a)
        else:
            return 0.0


if __name__ == '__main__':
    hd = HypergeometricDistribution(100, 25, 26)

    res={}
    for i in range(27):
        print(hd.p(i))