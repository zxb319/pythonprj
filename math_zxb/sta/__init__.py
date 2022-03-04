import math
from collections import Counter
from typing import List, Iterable

import math_zxb


def mode(elems: Iterable[float]):
    counter = Counter(elems)
    max_count = max(c for x, c in counter.items())
    return list((x, c) for x, c in counter.items() if c == max_count)


def median(elems: Iterable[float]):
    sorted_list = sorted(elems)
    if len(sorted_list) % 2 == 1:
        return sorted_list[len(sorted_list) // 2]
    else:
        i = len(sorted_list) // 2
        return (sorted_list[i - 1] + sorted_list[i]) / 2


def mean(elems: List[float]):
    return sum(elems) / len(elems)


def variance(elems: List[float]):
    m = mean(elems)
    return sum((x - m) ** 2 for x in elems) / (len(elems) - 1)


def std(elems: List[float]):
    return variance(elems) ** 0.5


def sample_range(elems: Iterable[float]):
    l = list(elems)
    return max(elems) - min(elems)


def skewness(elems: List[float]):
    m = mean(elems)
    return sum((x - m) ** 3 for x in elems) / (len(elems) - 1) / std(elems) ** 3


def kurtosis(elems: List[float]):
    m = mean(elems)
    return sum((x - m) ** 4 for x in elems) / (len(elems) - 1) / std(elems) ** 4 - 3

def corr(xs:List[float],ys:List[float]):
    x_bar = mean(xs)
    y_bar = mean(ys)

    a=sum((x-x_bar)*(y-y_bar) for x,y in zip(xs,ys))
    b=sum((x-x_bar)**2 for x in xs)
    c=sum((y-y_bar)**2 for y in ys)
    return a/(b*c)**0.5

def A(n: int, m: int):
    if m > n:
        return 0

    res = 1
    for i in range(m):
        res *= n - i
    return res


def C(n: int, m: int):
    return A(n, m) // A(m, m)


if __name__ == '__main__':
    xs=[300,400,500,500,800,1000,1000,1300]
    ys=[9500,10300,11000,12000,12400,13400,14500,15300]
    print(corr(xs,ys))
