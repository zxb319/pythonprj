import math_zxb
from math_zxb.sta.f_distribution import FDistribution
from math_zxb.sta.kai_distribution import KaiDistribution
from math_zxb.sta.normal_distribution import NormalDistribution
from math_zxb.sta.t_distribution import TDistribution


def miu_estimate_given_sigma(x_bar: float, sigma: float, p: float):
    pd = NormalDistribution(0, 1)
    lo, hi = pd.range_of(p)
    return x_bar - sigma * hi, x_bar - sigma * lo


def miu_estimate(n: int, x_bar: float, s: float, p: float):
    pd = TDistribution(n - 1)
    lo, hi = pd.range_of(p)
    return x_bar - s / n ** 0.5 * hi, x_bar - s / n ** 0.5 * lo


def sigma_estimate(n: int, s: float, p: float):
    pd = KaiDistribution(n - 1)

    lo, hi = pd.range_of(p)
    return ((n - 1) / hi) ** 0.5 * s, ((n - 1) / lo) ** 0.5 * s


def two_sigma_ratio_estimate(n1: int, s1: float, n2: int, s2: float, p: float):
    pd = FDistribution(n1 - 1, n2 - 1)
    lo, hi = pd.range_of(p)

    r = (s1 / s2) ** 2
    return r / hi, r / lo


def sample_size_estimate_for_diff_miu(h: float, s1: float, s2: float, p: float):
    pd = NormalDistribution(0, 1)
    return pd.range_of(p)[-1] ** 2 / h ** 2 * (s1 ** 2 + s2 ** 2)


def sample_size_estimate_for_diff_p(h: float, p1: float, p2: float, p: float):
    pd = NormalDistribution(0, 1)
    return pd.range_of(p)[-1] ** 2 / h ** 2 * (p1 * (1 - p1) + p2 * (1 - p2))


if __name__ == '__main__':
    s=(55.5/300)**0.5
    pd=TDistribution(23)
    lo,hi=pd.range_of(0.95)
    print(lo,hi)
    res=(7-hi*s,7-lo*s)

    print(res)

