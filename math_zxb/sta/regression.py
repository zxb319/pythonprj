from typing import List, Tuple

from math_zxb.sta import mean
from math_zxb.sta.f_distribution import FDistribution
from math_zxb.sta.t_distribution import TDistribution
import numpy as np


class SimpleLinearRegression:
    def __init__(self, xs: List[Tuple]):
        self._xs = xs
        self._x_bar = mean([x for x, y in xs])
        self._y_bar = mean([y for x, y in xs])
        self._ssxy = sum((x - self._x_bar) * (y - self._y_bar) for x, y in xs)
        self._ssx = sum((x - self._x_bar) ** 2 for x, y in xs)
        self._b1 = self._ssxy / self._ssx
        self._b0 = self._y_bar - self._b1 * self._x_bar

        self._ssr = sum((self._b0 + self._b1 * x - self._y_bar) ** 2 for x, y in self._xs)
        self._sst = sum((y - self._y_bar) ** 2 for _, y in self._xs)
        self._sse = self._sst - self._ssr
        self._r_squared = self._ssr / self._sst
        self._r = -self._r_squared ** 0.5 if self._b1 < 0 else self._r_squared ** 0.5

    @property
    def r_squared(self):
        return self._r_squared

    @property
    def r(self):
        return self._r

    def anova(self, alpha: float = 0.05):
        pd = FDistribution(1, len(self._xs) - 2)
        f = self._ssr / (self._sse / (len(self._xs) - 2))
        print(f)
        return 1 - pd.cp(f)

    def t_test(self, alpha: float = 0.05):
        t = self._b1 / (self._sse / (len(self._xs) - 2) / self._ssx) ** 0.5
        pd = TDistribution(len(self._xs) - 2)
        lo, hi = pd.range_of(1 - alpha)

        print(lo, hi, t)

        return 1 - pd.pbetween(-t, t)

    def predict(self, x):
        return self._b0 + self._b1 * x

    def __str__(self):
        if self._b1 < 0:
            return f"y={self._b0}{self._b1}*x"
        return f"y={self._b0}+{self._b1}*x"


class LinearRegression:
    def __init__(self, data: List[Tuple]):
        self._data = data
        A = np.matrix([(*x[:-1], 1) for x in data])
        b = np.matrix([x[-1] for x in data]).T

        at = A.T
        self._b = (at * A).I * at * b

        y_bar=mean([x[-1] for x in data])
        self._sst=sum((x[-1]-y_bar)**2 for x in data)

        y_hat=A*self._b-b
        self._ssr=sum((y-y_bar) for y in y_hat)
        self._sse=self._sst-self._ssr

        self._r_squared=self._ssr/self._sst
        self._adjusted_r_squared=1-(self._sse/(len(data)-len(self._b)))/(self._sst/(len(data)-1))

    @property
    def r_squared(self):
        return self._adjusted_r_squared

    def __str__(self):
        return str(self._b)


if __name__ == '__main__':
    xs = [
        (56, 64),
        (74, 80),
        (90, 82),
        (63, 68),
        (91, 89),
        (53, 61),
        (81, 76),
        (65, 70),
        (74, 80),
        (90, 93),
        (77, 71),
        (63, 58),
    ]

    lr=LinearRegression(xs)

    print(lr)
