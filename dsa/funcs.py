from collections import deque
from typing import Tuple, Union

from lintcode import *

import os


def sin(rad: Union[int, float]):
    xp = rad
    div = 1
    res = 0
    for i in range(30):
        res += xp / div
        xp = xp * (-1) * rad * rad
        div = div * (2 * i + 2) * (2 * i + 3)

    return res


def wanderFiles(dir: str, name: str, depth: int):
    print(" " * 4 * depth, name, sep="")
    if os.path.isdir(dir + name):
        paths = os.listdir(dir + name)
        for path in paths:
            wanderFiles(dir + name + "/", path, depth + 1)


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


def levelOrderTraverse(root: Node):
    if root is not None:
        queue: deque[Tuple[Node, int]] = deque()
        queue.append((root, 0))
        while len(queue) > 0:
            (curNode, curLevel) = queue.popleft()
            yield curNode, curLevel
            if curNode is None:
                continue
            for node in curNode.children:
                if node is None:
                    continue
                queue.append((node, curLevel + 1))


def inorder(root: TreeNode):
    if root.left:
        yield from inorder(root.left)
    yield root
    if root.right:
        yield from inorder(root.right)


def preorder(root: TreeNode):
    yield root
    if root.left:
        yield from preorder(root.left)
    if root.right:
        yield from preorder(root.right)


def postorder(root: TreeNode):
    if root.left:
        yield from postorder(root.left)
    if root.right:
        yield from postorder(root.right)
    yield root


def isPrime(num: int) -> bool:
    if num < 2: return False
    i = 2
    while i * i <= num:
        if num % i == 0: return False
        i += 1

    return True


if __name__ == "__main__":
    print(sin(3.1415926 / 3 * 2))
