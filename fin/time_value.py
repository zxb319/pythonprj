import math
from functools import reduce
from typing import List

from math_zxb import root_binarily


def effective_annual_rate(stated_annual_rate: float, pay_times_per_year: float):
    """
    :param stated_annual_rate:名义年化利率
    :param pay_times_per_year:每年结算次数
    :return: 实际年化利率
    """
    if pay_times_per_year is math.inf:
        return math.e ** stated_annual_rate - 1
    return (1 + stated_annual_rate / pay_times_per_year) ** pay_times_per_year - 1


def time_value(cash_flow: List[float], r: float, time_point: int = 0):
    """
    :param cash_flow: 现金流 cash_flow[0]表示第0期
    :param r:利率
    :param time_point:时期点
    :return:求给定time_point的现金值
    """
    return sum(a * (1 + r) ** (-i) for i, a in enumerate(cash_flow)) * (1 + r) ** time_point


def pv_of_perpetuity(annual: float, r: float):
    """
    :param annual: 年金
    :param r: 利率
    :return: 求永续年金的现值
    """
    return annual / r


def irr(cash_flow: List[float]):
    """
    :param cash_flow: 现金流 cash_flow[0]表示第0期
    :return:求给定现金流的内部收益率
    """

    def inner(r: float):
        return time_value(cash_flow, r, 0)

    return root_binarily(inner, -1 + 1e-10, 1e10)


def annuity(present_value: float, r: float, n: int):
    """
    :param present_value:现值
    :param r:利率
    :param n:期数
    :return:年金
    """
    return present_value * r / (1 - (1 + r) ** (-n))


def pay_times(present_value: float, r: float, annuity: float):
    return -math.log(1 - r * present_value / annuity) / math.log(1 + r)


def wait_times(pv, annual_pay, r, fv):
    """
    :param annual_pay: 年金
    :param pv:现值
    :param r:利率
    :param fv:终值
    :return:时间价值到达终值经历的期数
    """

    a = r * fv + annual_pay
    b = annual_pay + r * pv
    c = 1 + r

    return math.log(a / b, c)


def twr(hprs: List[float]):
    return reduce(lambda x, y: x * y, (1 + r for r in hprs), 1) ** (1 / len(hprs)) - 1


def debx(present_value: float, r: float, n: int):
    """
    :param present_value:
    :param r:
    :param n:
    :return:等额本息
    """
    bx = round(annuity(present_value, r, n), 2)
    res = []
    for i in range(1, n + 1):
        lx = round(present_value * r, 2)
        bj = round(bx - lx, 2)
        present_value -= bj
        present_value = round(present_value, 2)
        if i == n:
            bx = round(bx + present_value, 2)
            bj = round(bj + present_value, 2)
            present_value = 0

        res.append({
            "期数": i,
            "本期利息": lx,
            "本期本金": bj,
            "本期本息": bx,
            "剩余本金": present_value
        })

    return res


def debj(present_value: float, r: float, n: int):
    """
    :param present_value:
    :param r:
    :param n:
    :return: 等额本金
    """
    bj = round(present_value / n, 2)
    res = []
    for i in range(1, n + 1):
        lx = round(present_value * r, 2)
        bx = round(bj + lx, 2)
        present_value -= bj
        present_value = round(present_value, 2)
        if i == n:
            bx = round(bx + present_value, 2)
            bj = round(bj + present_value, 2)
            present_value = 0
        res.append({
            "期数": i,
            "本期利息": lx,
            "本期本金": bj,
            "本期本息": bx,
            "剩余本金": present_value
        })

    return res


if __name__ == '__main__':
    print(*debx(10000, 10 / 100 / 2, 10 * 2), sep='\n')
