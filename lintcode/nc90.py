def fib(n):
    if n in (0, 1):
        return n

    r = fib(n - 1) + fib(n - 2)
    print(n, r)
    return r


if __name__ == '__main__':
    print(fib(11))
