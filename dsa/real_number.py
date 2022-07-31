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


if __name__ == '__main__':
    a = lcm(8, 12)
    print(a)
