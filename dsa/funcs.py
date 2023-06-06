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
    files = os.listdir(dir)
    for f in files:
        file = os.path.join(dir, f)
        print(f'{"    " * depth}{f}')
        if os.path.isdir(file):
            wanderFiles(file, depth + 1)


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


import functools


class Loop:

    def __init__(self, times):
        self.times = times
        self.funcs = []
        self.args = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for i in range(self.times):
            print(rf'第{i + 1}次执行：')
            for f, a in zip(self.funcs, self.args):
                a_str = ','.join(str(x) for x in a['args']) + ',' + ','.join(rf"{k}={v}" for k, v in a['kwargs'])
                r = f(*a['args'], **a['kwargs'])
                print(rf"执行了{f.__name__}({a_str}):结果为:{r}")
        pass

    def __getattr__(self, item):
        def dec_func(func):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                self.args.append({
                    'args': args,
                    'kwargs': kwargs,
                })

            return inner

        f = globals().get(item)
        print(*globals().items(),sep='\n')
        self.funcs.append(f)

        return dec_func(f)


if __name__ == "__main__":
    with Loop(times=3) as a:
        a.isPrime(2)
        a.gcd(8, 12)
    #
    # print(*globals().items(),sep='\n')
