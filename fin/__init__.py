import math
from functools import reduce
from typing import List

from math_zxb import root_binarily


def ear(rs: float, m: float):
    """
    :param rs: stated annual interest rate
    :param m: compounded count per year
    :return: effective annual interest rate
    """
    if m is math.inf:
        return math.e ** rs - 1
    return (1 + rs / m) ** m - 1


def time_value(cash_flow: List[float], r: float, time_point: int):
    return sum(a * (1 + r) ** (-i) for i, a in enumerate(cash_flow)) * (1 + r) ** time_point


def pv_of_perpetuity(annual: float, r: float):
    return annual / r


def irr(cash_flow: List[float]):
    def inner(r: float):
        return time_value(cash_flow, r, 0)

    return root_binarily(inner, 0 + 1e-10, 1e10)


def annuity(present_value: float, r: float, n: int):
    return present_value * r / (1 - (1 + r) ** (-n))


def period_count(present_value: float, r: float, annuity: float):
    return -math.log(1 - r * present_value / annuity)/math.log(1 + r)


def twr(hprs: List[float]):
    return reduce(lambda x, y: x * y, (1 + r for r in hprs), 1) ** (1 / len(hprs)) - 1


def debx(present_value: float, r: float, n: int):
    a = annuity(present_value, r, n)
    res = []
    for i in range(1, n + 1):
        lx = present_value * r
        bj = a - lx
        present_value -= bj
        res.append({
            "期数": i,
            "本期利息": lx,
            "本期本金": bj,
            "本期本息": a,
            "剩余本金": present_value
        })

    return res


def debj(present_value: float, r: float, n: int):
    bj = present_value / n
    res = []
    for i in range(1, n + 1):
        lx = present_value * r
        a = bj + lx
        present_value -= bj
        res.append({
            "期数": i,
            "本期利息": lx,
            "本期本金": bj,
            "本期本息": a,
            "剩余本金": present_value
        })

    return res


if __name__ == '__main__':
    a=1505
    p=30_0000
    r=0.06/12
    print(p*r)
    n=period_count(p,r,a)
    print(n/12)
