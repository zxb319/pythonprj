def fib(n):
    if n in (0, 1):
        return n
    return fib(n - 1) + fib(n - 2)


if __name__ == '__main__':
    print(fib(10))




