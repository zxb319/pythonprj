class UniformDistribution:
    def __init__(self, alpha: float, beta: float):
        assert alpha < beta

        self._alpha = alpha
        self._beta = beta

    def cp(self, x: float):
        if x < self._alpha:
            return 0
        if self._beta < x:
            return 1
        return (x - self._alpha) / (self._beta - self._alpha)

    def pbetween(self, lo: float, hi: float):
        return self.cp(hi) - self.cp(lo)

    def miu(self):
        return (self._alpha + self._beta) / 2

    def sigma(self):
        res = (self._beta - self._alpha) ** 2 / 12
        return res ** 0.5


if __name__ == '__main__':
    pd = UniformDistribution(0, 30)
    print(pd.cp(5))
    print(1 - pd.cp(10))
