import math


class Dist:
    def cp(self, x: float):
        raise NotImplementedError()

    def pbetween(self, lo: float, hi: float):
        raise NotImplementedError()

    def x_of(self, p: float):
        raise NotImplementedError()

    def range_of(self, p: float):
        raise NotImplementedError()

    def miu(self):
        raise NotImplementedError()

    def sigma(self):
        raise NotImplementedError()


class PowerDist:
    def __init__(self, theta: float):
        self._theta = theta

        def f(x: float):
            return 1 / theta * math.e ** (-x / theta)

        self._pdf=f

    def miu(self):
        return self._theta

    def sigma(self):
        return self._theta

