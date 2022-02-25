from typing import List


def factors(num: int):
    if num < 0:
        raise ArithmeticError("num must >0")

    if num <= 1:
        return {num: 1}

    res = {}
    while num > 1:
        f = 2
        while f <= num:
            if num % f == 0:
                res[f] = res.get(f, 0) + 1
                num //= f
                break

            f += 1

    return res


def lcm(a: int, b: int):
    """最小公倍数"""
    afs = factors(a)
    bfs = factors(b)
    for f, c in bfs.items():
        if f not in afs or afs[f] < c:
            afs[f] = c

    res = 1
    for f, c in afs.items():
        res *= f ** c

    return res


class _Term:
    def __init__(self, int_part: int, base: int, power: int):

        base_factors = factors(base)

        for f, c in base_factors.items():
            if c % power == 0:
                base //= f ** c
                int_part *= f ** (c // power)

        if int_part==0 or base==0:
            int_part=0
            base=0

        if base in (0,1):
            power=1

        self._int_part = int_part
        self._base = base
        self._power = power

    def __str__(self):
        return f"{self._int_part}*{self._power}√{self._base}"

    def __neg__(self):
        return _Term(-self._int_part, self._base, self._power)

    def __mul__(self, other: "_Term"):
        lcm_num = lcm(self._power, other._power)

        int_part=self._int_part * other._int_part
        base=self._base ** (lcm_num // self._power) * other._base ** (lcm_num // other._power)

        return _Term(int_part,base,lcm_num)


if __name__ == '__main__':
    a = _Term(1, 9, 2)
    b = _Term(1, 9, 2)

    print(a * b)
    # print(factors(18))