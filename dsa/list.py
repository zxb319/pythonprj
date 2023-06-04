from typing import Any


class _Node:
    def __init__(self, val: Any, next=None, pre=None):
        self.val = val
        self.next: _Node = next
        self.pre: _Node = pre

    def __str__(self):
        return str(self.val)


class List:
    __slots__ = {"__head", "__tail", "__count"}

    def __init__(self):
        self.__head: _Node = None
        self.__tail: _Node = None
        self.__count: int = 0

    def addFirst(self, val: Any):
        newNode = _Node(val)
        if self.__count == 0:
            self.__head = newNode
            self.__tail = newNode
            self.__head.next = self.__tail
            self.__tail.pre = self.__head
        else:
            newNode.next = self.__head
            self.__head.pre = newNode
            self.__head = newNode

        self.__count += 1

    def addLast(self, val: Any):
        newNode = _Node(val)
        if self.__count == 0:
            self.__head = newNode
            self.__tail = newNode
            self.__head.next = self.__tail
            self.__tail.pre = self.__head
        else:
            newNode.pre = self.__tail
            self.__tail.next = newNode
            self.__tail = newNode

        self.__count += 1

    def delFirst(self):
        if self.__count == 0:
            raise IndexError("List:empty!")

        if self.__count == 1:
            res = self.__head.val
            self.__head = None
            self.__tail = None
        else:
            res = self.__head.val
            newHead = self.__head.next
            newHead.pre = None
            self.__head = newHead
        self.__count -= 1
        return res

    def delLast(self):
        if self.__count == 0:
            raise IndexError("List:empty!")

        if self.__count == 1:
            res = self.__head.val
            self.__head = None
            self.__tail = None
        else:
            res = self.__tail.val
            newTail = self.__tail.pre
            newTail.next = None
            self.__tail = newTail

        self.__count -= 1
        return res

    def __len__(self):
        return self.__count

    def __str(self, h: _Node):
        if h is None:
            return "None"
        else:
            return str(h) + "->" + self.__str(h.next)

    def __str__(self):
        return self.__str(self.__head)


if __name__ == "__main__":
    l = List()
    for i in range(10):
        l.addFirst(i)
        l.addLast(i * i)

    l.delLast()
    l.delFirst()
    print(l)
