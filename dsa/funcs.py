import os


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


def wanderFiles(dir: str, depth: int):
    files=os.listdir(dir)
    for f in files:
        file=os.path.join(dir,f)
        print(f'{"    "*depth}{f}')
        if os.path.isdir(file):
            wanderFiles(file,depth+1)


def gcd(a: int, b: int) -> int:
    while a != 0:
        newa = b % a
        b = a
        a = newa

    return b


def fib():
    f0 = 0
    f1 = 1
    yield f0
    yield f1
    while True:
        f1 += f0
        f0 = f1 - f0
        yield f1


def isPrime(num: int) -> bool:
    if num < 2: return False
    i = 2
    while i * i <= num:
        if num % i == 0: return False
        i += 1

    return True


if __name__ == "__main__":
    dir=os.path.abspath(__file__)
    dir=os.path.dirname(dir)
    dir=os.path.dirname(dir)
    wanderFiles(dir,0)
