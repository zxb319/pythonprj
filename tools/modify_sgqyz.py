import functools


def cache(func):
    c = dict()

    @functools.wraps(func)
    def inner(a):
        if a in c:
            return c[a]
        r = func(a)
        c[a] = r
        return r

    return inner


import dsa.run_time


@dsa.run_time.run_time
# @cache
def fib(n):
    if n in (0, 1):
        return n
    return fib(n - 1) + fib(n - 2)


if __name__ == '__main__':
    import dsa

    print(fib(40))
