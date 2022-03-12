from math_zxb import root_binarily

E = 2.718281828459045

PI = 3.141592653589793


def absolute(num: float):
    return -num if num < 0 else num


def square_root(num: float):
    x = 1
    new_x = (x + num / x) / 2

    while new_x != x:
        x = new_x
        new_x = (x + num / x) / 2

    return x


def _power_int(b: float, p: int):
    if p == 0:
        return 1
    if p < 0:
        return 1 / _power_int(b, -p)
    if p % 2 == 1:
        return b * _power_int(b, p - 1)

    return _power_int(b * b, p // 2)


def power(b: float, p: float):
    assert b >= 0

    while True:
        if p == 0.0:
            return 1
        elif p < 0:
            return 1 / power(b, -p)

        elif p < 1:
            b = square_root(b)
            p *= 2

        else:
            int_part = int(p)
            point_part = p - int_part

            return _power_int(b, int_part) * power(b, point_part)


def logarithm(b: float, num: float):
    assert num > 0 and b > 0 and b != 1

    def f(x: float):
        return power(b, x) - num

    if b < 1 and num < 1:
        lo = 0
        hi = 1
        while power(b, hi) > num:
            hi *= 2

        return root_binarily(f, lo, hi)

    elif b < 1 and num >= 1:
        lo = -1
        hi = 0
        while power(b, lo) < num:
            lo *= 2

        return root_binarily(f, lo, hi)

    elif b >= 1 and num < 1:
        lo = -1
        hi = 0
        while power(b, lo) > num:
            lo *= 2

        return root_binarily(f, lo, hi)

    else:
        lo = 0
        hi = 1
        while power(b, hi) < num:
            hi *= 2

        return root_binarily(f, lo, hi)


def sine(x: float):
    x-=int(x/(2*PI))*2*PI
    res = 0
    i = 1
    term = x
    while True:
        if term == 0.0:
            return res
        res += term
        term *= x * x
        term /= (i + 1) * (i + 2)
        term *= -1
        i += 2


def cosine(x: float):
    x-=int(x/(2*PI))*2*PI
    res = 0
    i = 1
    term = 1
    while True:
        if term == 0.0:
            return res
        res += term
        term *= x * x
        term /= i * (i + 1)
        term *= -1
        i += 2


def arcsine(x: float):
    def f(r: float):
        return sine(r) - x

    return root_binarily(f, -PI / 2, PI / 2)


def arccosine(x: float):
    def f(r: float):
        return cosine(r) - x

    return root_binarily(f, 0, PI)


if __name__ == '__main__':
    a = sine(PI / 6)
    print(a)
