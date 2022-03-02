from math_zxb.sta import mean, std
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
    xs1=[73,65,68,80,72,75,69,58,67,66,88]

    s1=std(xs1)
    n1=len(xs1)

    xs2=[80,70,64,73,61,55,67,82,65,57,74]

    s2=std(xs2)
    n2=len(xs2)

    pd=FDistribution(n1-1,n2-1)

    f=s1**2/s2**2

    lo,hi=pd.range_of(0.95)

    print(lo,hi,f)
