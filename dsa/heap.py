import heapq
from collections.abc import Callable
from typing import Any, Iterable


class Heap:
    """
    默认最小堆
    """
    __slots__ = {"__dat", "__keyFunc", "__unique", "__cache"}

    def __init__(self, elems: Iterable = [], keyFunc: Callable = None, unique: bool = False):
        if keyFunc is None:
            self.__keyFunc: Callable = lambda x: x
        else:
            self.__keyFunc: Callable = keyFunc

        self.__unique = unique

        self.__cache = set()
        if not self.__unique:
            self.__dat: list = [(self.__keyFunc(x), x) for x in elems]
            heapq.heapify(self.__dat)
        else:
            self.__dat: list = []
            for val in elems:
                if val not in self.__cache:
                    heapq.heappush(self.__dat, (self.__keyFunc(val), val))
                    self.__cache.add(val)

    def top(self):
        return self.__dat[0][1]

    def push(self, val: Any):
        if self.__unique and val not in self.__cache or not self.__unique:
            heapq.heappush(self.__dat, (self.__keyFunc(val), val))

        if self.__unique:
            self.__cache.add(val)

    def pop(self):
        if self.top() in self.__cache:
            self.__cache.remove(self.top())

        return heapq.heappop(self.__dat)[1]

    def __len__(self):
        return len(self.__dat)

    def __str__(self):
        return str(list(x[1] for x in self.__dat))


if __name__ == "__main__":
    heap = Heap([1, 2, 3], keyFunc=lambda x: -x, unique=True)
    for i in reversed(range(10)):
        heap.push(i * i)

    print(heap)
