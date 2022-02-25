from math_zxb.sta import C


class NegBinDistribution:
    def __init__(self, r: int, p_success: float):
        """r:成功次数"""
        if not 0 < r:
            raise ArithmeticError("r>0 is must")

        self._r = r
        self._p_success = p_success

    def p(self, y: int):
        if y < self._r:
            return 0.0

        return C(y - 1, self._r - 1) * self._p_success ** (self._r) * (1 - self._p_success) ** (y - self._r)


if __name__ == '__main__':
    pd = NegBinDistribution(1,0.1)

    res=0
    for i in range(10):
        p=pd.p(i)
        res+=p
        print(i,p,res)
