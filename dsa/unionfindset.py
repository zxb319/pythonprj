from typing import Any, Dict


class _Node:
    __slots__ = {"parent", "count"}

    def __init__(self):
        self.parent = self
        self.count = 1


class UnionFindSet:
    __slots__ = {"__map"}

    def __init__(self):
        self.__map: Dict[Any, _Node] = {}

    def __nodeOf(self, p) -> _Node:
        if p not in self.__map:
            self.__map[p] = _Node()

        return self.__map[p]

    def __rootOf(self, p) -> _Node:
        node = self.__nodeOf(p)
        while node.parent != node:
            node.parent = node.parent.parent
            node = node.parent

        return node

    def isConnected(self, p, q) -> bool:
        return self.__rootOf(p) == self.__rootOf(q)

    def connect(self, p, q) -> None:
        rootP = self.__rootOf(p)
        rootQ = self.__rootOf(q)
        if rootP == rootQ: return
        if rootP.count < rootQ.count:
            rootP.parent = rootQ
            rootQ.count += rootP.count
        else:
            rootQ.parent = rootP
            rootP.count += rootQ.count

    def distinctSetsCount(self) -> int:
        return len(set(self.__rootOf(n) for n in self.__map))
