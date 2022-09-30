from functools import total_ordering


def gcd(a: int, b: int):
    while a != 0:
        tmp = b % a
        b = a
        a = tmp

    return b


@total_ordering
class Fraction:
    def __init__(self, num: int = 0, denom: int = 1):
        if denom == 0:
            raise ArithmeticError("denom!=0 is must.")

        g = gcd(num, denom)
        num //= g
        denom //= g

        if denom < 0:
            num = -num
            denom = -denom

        self._num = num
        self._denom = denom

    def __str__(self):
        return f"{self._num}/{self._denom}"

    @property
    def rep(self):
        return Fraction(self._denom, self._num)

    def __neg__(self):
        return Fraction(-self._num, self._denom)

    def __add__(self, other: "Fraction"):
        return Fraction(self._num * other._denom + self._denom * other._num, self._denom * other._denom)

    def __sub__(self, other: "Fraction"):
        return self + -other

    def __mul__(self, other: "Fraction"):
        return Fraction(self._num * other._num, self._denom * other._denom)

    def __truediv__(self, other: "Fraction"):
        return self * other.rep

    def __lt__(self, other: "Fraction"):
        return self._num * other._denom < self._denom * other._num

    def __eq__(self, other: "Fraction"):
        return self._num == other._num and self._denom == other._denom

    def __pow__(self, power: int, modulo=None):
        if power == 0:
            return Fraction(1, 1)
        if power < 0:
            return Fraction(1, 1) / self ** (-power)

        if power % 2 == 0:
            return (self * self) ** (power // 2)

        return self * self ** (power - 1)

    def __float__(self):
        return self._num/self._denom


if __name__ == '__main__':
    f0 = Fraction(2244851485148514627, 8118811881188118000)
    f1 = Fraction(3, 9)

    print(f0)
