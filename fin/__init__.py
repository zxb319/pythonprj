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

    return root_binarily(inner, -1 + 1e-10, 1e10)


def annuity(present_value: float, r: float, n: int):
    return present_value * r / (1 - (1 + r) ** (-n))


def period_count(present_value: float, r: float, annuity: float):
    return -math.log(1 - r * present_value / annuity, 1 + r)


def twr(hprs: List[float]):
    return reduce(lambda x, y: x * y, (1 + r for r in hprs), 1) ** (1 / len(hprs)) - 1


if __name__ == '__main__':
    print()