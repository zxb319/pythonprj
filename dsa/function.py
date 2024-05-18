from typing import Iterable, Callable, Any


class EnIterable:
    __slots__ = {"__inputs"}

    def __init__(self, inputs: Iterable):
        self.__inputs = inputs

    def map(self, f: Callable[[Any], Any]) -> "EnIterable":
        return EnIterable(f(x) for x in self)

    def filter(self, f: Callable[[Any], bool]) -> "EnIterable":
        return EnIterable(x for x in self if f(x))

    def __firstn(self, n: int):
        for i, x in enumerate(self):
            yield x
            if i == n - 1:
                break

    def take(self, n: int) -> "EnIterable":
        return EnIterable(self.__firstn(n))

    def drop(self, n: int) -> "EnIterable":
        return EnIterable(x for i, x in enumerate(self) if i >= n)

    def reduce(self, f: Callable[[Any, Any], Any], init):
        res = init
        for x in self:
            res = f(res, x)
        return res

    def foreach(self, f: Callable[[Any], None]):
        for x in self:
            f(x)

    def __iter__(self):
        return (x for x in self.__inputs)


if __name__ == '__main__':
    pass
