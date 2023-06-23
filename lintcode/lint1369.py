class Cache:
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args, **kwargs):
        k = rf'{args},{kwargs}'
        if k in self.cache:
            return self.cache[k]
        r = self.func(*args, **kwargs)
        self.cache[k] = r
        return r


@Cache
def fib(n):
    if n in (0, 1):
        return n
    return fib(n - 1) + fib(n - 2)


if __name__ == '__main__':
    print(fib(12))
    print(fib.cache)
