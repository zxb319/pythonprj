from math_zxb.sta import mean, std, corr
from math_zxb.sta.distributions import Dist
from math_zxb.sta.f_distribution import FDistribution
from math_zxb.sta.kai_distribution import KaiDistribution
from math_zxb.sta.normal_distribution import NormalDistribution
from math_zxb.sta.t_distribution import TDistribution


def left_tail_test_miu(pd: "Dist", z:float, alpha: float):
    """pd只能用标准正态分布或者T分布"""
    critical_x = pd.x_of(alpha)
    pvalue=pd.cp(z)
    print(critical_x,z)
    print(f"p-value={pvalue}")
    return z < critical_x


def right_tail_test_miu(pd: "Dist", z:float, alpha: float):
    """pd只能用标准正态分布或者T分布"""
    critical_x = pd.x_of(1 - alpha)
    pvalue=1-pd.cp(z)
    print(critical_x,z)
    print(f"p-value={pvalue}")
    return z > critical_x


def doule_tail_test_miu(pd: "Dist", z:float, alpha: float):
    """pd只能用标准正态分布或者T分布"""
    lo, hi = pd.range_of(1 - alpha)
    pvalue=1-abs(pd.cp(z)-pd.cp(-z))
    print(lo,hi,z)
    print(f"p-value={pvalue}")
    return z < lo or z > hi


def left_tail_test_sigma(n: int, s: float, sigma: float, alpha: float):
    pd=KaiDistribution(n-1)
    x = pd.x_of(alpha)
    chi = (n - 1) * s ** 2 / sigma ** 2
    pvalue=pd.cp(chi)
    print(x,chi)
    print(f"p-value={pvalue}")
    return chi < x


def right_tail_test_sigma(n: int, s: float, sigma: float, alpha: float):
    pd = KaiDistribution(n - 1)
    x = pd.x_of(1 - alpha)
    chi = (n - 1) * s ** 2 / sigma ** 2
    pvalue=1-pd.cp(chi)
    print(x,chi)
    print(f"p-value={pvalue}")
    return chi > x


def double_tail_test_sigma(n: int, s: float, sigma: float, alpha: float):
    pd = KaiDistribution(n - 1)
    lo, hi = pd.range_of(1 - alpha)
    chi = (n - 1) * s ** 2 / sigma ** 2

    print(lo,hi,chi)
    return chi < lo or chi > hi


if __name__ == '__main__':
    xs=[300,400,500,500,800,1000,1000,1300]
    ys=[9500,10300,11000,12000,12400,13400,14500,15300]
    r=corr(xs,ys)
    print(r)

    t=r/((1-r**2)/(len(xs)-2))**0.5

    print(t)

    pd=TDistribution(len(xs)-2)

    print(pd.range_of(0.99))
    pvalue=1-pd.pbetween(-t,t)

    print(pvalue)