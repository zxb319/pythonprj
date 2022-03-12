import sys

# sys.path.append('..')

import heapq
import random
import re
from functools import cmp_to_key
from typing import List
from collections import Counter, deque
from math import sqrt
from random import randint
from collections import OrderedDict

# from dsa.fraction import Fraction
from leetcode import *
from dsa.heap import Heap


class Solution:
    def preorderTraversal(self, root: TreeNode) -> List[int]:
        # write code here
        return list(self.preorder(root))

    def preorder(self,root: TreeNode):
        if root:
            yield root.val
            yield from self.preorder(root.left)
            yield from self.preorder(root.right)

class Solution:
    def printListFromTailToHead(self , listNode: ListNode) -> List[int]:
        # write code here
        res=deque()
        while listNode is not None:
            res.appendleft(listNode.val)

        return res

class Solution:
    def __init__(self):
        self._mp = {}

    def Sum_Solution(self, n: int) -> int:
        # write code here
        if n in self._mp:
            return self._mp[n]
        if n == 0:
            return 0
        res = self.Sum_Solution(n - 1) + n
        self._mp[n] = res
        return res


class Solution:
    def __init__(self):
        self._mp = {}

    def jumpFloorII(self, number: int) -> int:
        # write code here
        if number in self._mp:
            return self._mp[number]
        if number == 0:
            return 1
        res = sum(self.jumpFloorII(i) for i in range(number))
        self._mp[number] = res
        return res


class Solution:
    def minNumberDisappeared(self, nums: List[int]) -> int:
        # write code here
        s = set(nums)
        res = 1
        while True:
            if res not in s:
                return res
            res += 1


class Solution:
    """
    @param moves: a sequence of its moves
    @return: if this robot makes a circle
    """
    mp = {
        'U': (0, 1),
        'D': (0, -1),
        'L': (-1, 0),
        'R': (1, 0)
    }

    def judgeCircle(self, moves):
        a = [self.mp[c] for c in moves]

        x = sum(i[0] for i in a)
        y = sum(i[1] for i in a)

        return x == 0 and y == 0


class Solution:
    def Print(self, pRoot: TreeNode) -> List[List[int]]:

        if not pRoot:
            return []
        # write code here
        od = OrderedDict()
        queue = deque()
        queue.append((pRoot, 0))
        while len(queue) > 0:
            cur, depth = queue.popleft()
            if depth in od:
                od[depth].append(cur)
            else:
                od[depth] = [cur]
            if cur.left:
                queue.append((cur.left, depth + 1))
            if cur.right:
                queue.append((cur.right, depth + 1))

        return [x for x in od.items()]


class Solution:
    coins = [1, 5, 10, 25]
    res = []

    def waysToChange(self, n: int) -> int:
        if n < 0:
            return 0
        if n == 1:
            return 1

        if len(self.res) > n:
            return self.res[n]

        for i in range(len(self.res), n + 1):
            rrr = 0
            if i >= 1:
                rrr += self.res[i - 1]
            if i >= 5:
                rrr += self.res[i - 5]
            if i >= 10:
                rrr += self.res[i - 10]
            if i >= 25:
                rrr += self.res[i - 25]
            self.res.append(rrr)

        return self.res[-1]


class Solution:
    def FirstNotRepeatingChar(self, str: str) -> int:
        # write code here
        mp = dict()
        for i, c in enumerate(str):
            mp[c] = i
        od = OrderedDict()
        for c in str:
            od[c] = od.get(c, 0) + 1

        for c, num in od.items():
            if num == 1:
                return mp[c]


class Solution:
    def Mirror(self, pRoot: TreeNode):
        # write code here
        if not pRoot:
            return pRoot

        a = self.Mirror(pRoot.left)
        b = self.Mirror(pRoot.right)

        pRoot.left = b
        pRoot.right = a
        return pRoot


class Solution:
    def GetNumberOfK(self, data: List[int], k: int) -> int:
        # write code here
        pos = self.find(data, k, 0, len(data)) - 1
        res = 0
        while pos >= 0 and data[pos] == k:
            res += 1

        return res

    def find(self, data: List[int], k: int, lo: int, hi: int):
        if lo >= hi:
            return lo

        mi = (lo + hi) // 2
        if k < data[mi]:
            return self.find(data, k, lo, mi)
        else:
            return self.find(data, k, mi + 1, hi)


class Solution:
    def solve(self, nums):
        if all(x == 0 for x in nums):
            return '0'

        # write code here
        def cmp(x: int, y: int):
            a = str(x)
            b = str(y)
            return -int(a + b) + int(b + a)

        a = sorted(nums, key=cmp_to_key(cmp))
        return ''.join(str(x) for x in a)


class Solution:
    def sortInList(self, head: ListNode):
        # write code here
        if not head:
            return head

        l = []
        cur = head

        while cur:
            l.append(cur)
            cur = cur.next

        res = sorted(l, key=lambda node: node.val)

        for i in range(0, len(l) - 1):
            l[i].next = l[i + 1]

        l[-1].next = None
        return l[0]


class Solution:
    def longestCommonPrefix(self, strs):
        # write code here
        max_prefix_indx = 0
        res = []
        for c in strs[0]:
            for s in strs[1:]:
                if max_prefix_indx >= len(s):
                    return ''.join(res)
                if s[max_prefix_indx] != strs[0][max_prefix_indx]:
                    return ''.join(res)
            res.append(c)
            max_prefix_indx += 1

        return ''.join(res)


class Solution:
    def KthNode(self, proot: TreeNode, k: int) -> int:
        # write code here
        for i, v in enumerate(self.mid_traverse(proot)):
            if i == k - 1:
                return v

    def mid_traverse(self, root: TreeNode):
        if root:
            if root.left:
                yield from self.mid_traverse(root.left)

            yield root.val

            if root.right:
                yield from self.mid_traverse(root.right)


class Solution:
    def FindNumsAppearOnce(self, array):
        # write code here
        counter = Counter(array)
        return list(k for k, v in counter.items() if v == 1)


class Solution:
    def topKstrings(self, strings: List[str], k: int):
        # write code here
        counter = Counter(strings)
        heap = Heap(keyFunc=lambda x: (x[1], [-ord(c) for c in x[0]]))
        for s, c in counter.items():
            if len(heap) < k:
                heap.push((s, c))
            elif (-heap.top()[1], heap.top()[0]) > (c, s):
                heap.pop()
                heap.push((s, c))

        res = []
        while len(heap) > 0:
            res.append(heap.pop())

        return list(reversed(res))


if __name__ == '__main__':
    s = Solution()
    a = s.topKstrings(["abcd", "abcd", "abcd", "pwb2", "abcd", "pwb2", "p12"], 3)
    print(a)
