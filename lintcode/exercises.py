import functools


def cache(func):
    c = dict()

    @functools.wraps(func)
    def inner(*args, **kwargs):
        print(args, kwargs)
        key = tuple(list(args) + [v for k, v in sorted(kwargs.items())])
        if key in c:
            return c[key]

        r = func(*args, **kwargs)
        c[key] = r

        return r

    return inner


@cache
def fib(n):
    if n in (0, 1):
        return n
    return fib(n - 1) + fib(n - 2)


if __name__ == '__main__':
    r = fib(100)
    print(r)

    print(2**68)
