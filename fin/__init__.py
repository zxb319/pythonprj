from typing import List

from math_zxb import root_binarily


def ear(rs: float, m: int):
    """
    :param rs: stated annual interest rate
    :param m: compounded count per year
    :return: effective annual interest rate
    """
    return (1 + rs / m) ** m


def pv(cash_flow: List[float], r: float):
    return sum(a * (1 + r) ** (-i) for i, a in enumerate(cash_flow))


def irr(cash_flow: List[float]):
    def inner(r: float):
        return pv(cash_flow, r)

    return root_binarily(inner, -1 + 1e-10, 1e10)


if __name__ == '__main__':
    a = irr([-100, 20, 20, 20, 20])
    print(a)
