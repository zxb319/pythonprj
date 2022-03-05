from math_zxb.zxb import square_root, arcsine, PI, power, sine, cosine


class Complex:
    def __init__(self, real: float = 0, imag: float = 0):
        self._real = real
        self._imag = imag

    def __str__(self):
        if self._imag < 0:
            return f"{self._real}{self._imag}i"
        else:
            return f"{self._real}+{self._imag}i"

    @property
    def conj(self):
        return Complex(self._real, -self._imag)

    def __neg__(self):
        return Complex(-self._real, -self._imag)

    def __add__(self, other: "Complex"):
        return Complex(self._real + other._real, self._imag + other._imag)

    def __sub__(self, other: "Complex"):
        return self + -other

    def __mul__(self, other: "Complex"):
        return Complex(self._real * other._real - self._imag * other._imag,
                       self._real * other._imag + self._imag * other._real)

    def __truediv__(self, other: "Complex"):
        c = self * other.conj
        d = (other * other.conj)._real
        return Complex(c._real / d, c._imag / d)

    def __abs__(self):
        return square_root(self._real * self._real + self._imag * self._imag)

    @property
    def arc(self):
        length = abs(self)
        res = arcsine(self._imag / length)
        if self._real >= 0 and self._imag >= 0:
            return res
        elif self._real < 0 and self._imag >= 0:
            return PI - res
        elif self._real < 0 and self._imag < 0:
            return PI - res
        else:
            return 2 * PI + res

    def __pow__(self, p: float, modulo=None):
        arc = self.arc * p
        length = power(abs(self), p)
        return Complex(length * cosine(arc), length * sine(arc))

    def pow_root(self, p: int):
        assert p > 1
        res = []
        length = abs(self) ** (1 / p)
        arc = self.arc
        for i in range(p):
            carc = (arc + 2 * i * PI) / p
            res.append(Complex(length * cosine(carc), length * sine(carc)))

        return res


if __name__ == '__main__':
    c = Complex(-1, 1)
    print(c.__pow__(-1))

