from collections import Counter
from typing import List, Iterable


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


if __name__ == '__main__':
    a = [5, 8, 1, 2, 4]
    print(mean(a))
    print(variance(a))
    print(std(a))
