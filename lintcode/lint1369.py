from random import *

from leetcode import *

from functools import reduce

from typing import *

from collections import deque

import re

import heapq

from dsa.funcs import isPrime
from collections import Counter

from dsa.math.line import *

from dsa.heap import Heap

from dsa.unionfindset import UnionFindSet

from math import sqrt

from threading import Lock


class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        a = Counter(nums)
        return [num for num, cnt in a.items() if cnt > len(nums) // 3]


class Solution:
    def oddEvenList(self, head: ListNode) -> ListNode:
        a = self.trav(head)
        b = self.trav(head.next)

        c = self.merge(a, b)

        newHead = next(c)
        cur = newHead
        for e in c:
            cur.next = e
            cur = cur.next

        return newHead

    def merge(self, a: Iterable, b: Iterable):
        yield from a
        yield from b

    def trav(self, head: ListNode):
        while head:
            yield head
            head = head.next
            if not head: break
            head = head.next


class Solution:
    def removeZeroSumSublists(self, head: ListNode) -> ListNode:
        a = []
        accSum = 0
        while head:
            accSum += head.val
            a.append((accSum, head))

        pos = len(a) - 1

        while pos >= 0 and a[pos] != 0:
            pos -= 1

        a = a[pos + 1:]

        cache = dict()
        for accSum, node in a:
            if accSum in cache:
                cache[accSum].next = node.next

        return a[0][1]


class Foo:
    def __init__(self):
        self.lock = Lock()
        self.cnt = 0

    def first(self, printFirst: 'Callable[[], None]') -> None:
        # printFirst() outputs "first". Do not change or remove this line.
        self.lock.acquire(True)
        if self.cnt % 3 == 0:
            printFirst()
            self.cnt += 1
        self.lock.release()

    def second(self, printSecond: 'Callable[[], None]') -> None:
        # printSecond() outputs "second". Do not change or remove this line.
        self.lock.acquire(True)
        if self.cnt % 3 == 1:
            printSecond()
            self.cnt += 1
        self.lock.release()

    def third(self, printThird: 'Callable[[], None]') -> None:
        # printThird() outputs "third". Do not change or remove this line.
        self.lock.acquire(True)
        if self.cnt % 3 == 2:
            printThird()
            self.cnt += 1
        self.lock.release()


class Solution:
    def subSort(self, array: List[int]) -> List[int]:
        newArr = sorted(array)
        f = 0
        while f < len(array) and newArr[f] == array[f]:
            f += 1

        t = len(array) - 1
        while t >= 0 and newArr[t] == array[t]:
            t -= 1

        return [-1, -1] if t <= f else [f, t]


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        start = 0
        cache = dict()
        res = 1
        for i, c in enumerate(s):
            if c not in cache or cache[c] < start:
                pass
            else:
                start = cache[c] + 1

            if res < i - start + 1:
                res = i - start + 1

        return res


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        a = ((self.keyOfstr(s), s) for s in strs)
        d = dict()
        for key, itm in a:
            if key in d:
                d[key].append(itm)
            else:
                d[key] = [itm]

        return [itm for itm in d.values()]

    def keyOfstr(self, s: str):
        a = Counter(s)
        return ','.join(sorted(c + ":" + str(i) for c, i in a.items()))


class Solution:
    def validIPAddress(self, IP: str) -> str:
        if self.isIpv4(IP):
            return 'IPv4'
        elif self.isIpv6(IP):
            return 'IPv6'
        else:
            'Neither'

    def isIpv4(self, ip: str):
        a = ip.split('.')
        if len(a) != 4: return False
        for i in a:
            if a == '': return False
            if not 0 <= int(i) <= 255: return False
            if i != '0' and i.startswith('0'): return False

        return True

    def isIpv6(self, ip: str):
        a = ip.split(':')
        if len(a) != 8: return False
        for i in a:
            if a == '': return False
            if not re.match(r'^[0-9a-zA-Z]{1,4}$', i): return False

        return True


class Solution:
    def minNumber(self, nums: List[int]) -> str:
        nums = sorted(nums, key=lambda x: [ord('9') - ord(d) for d in str(x)])
        return ''.join(nums)


class Solution:
    def minDifference(self, nums: List[int]) -> int:
        if len(nums) <= 4: return 0
        nums = sorted(nums)
        a = nums[-4] - nums[0]
        if nums[-3] - nums[1] < a:
            a = nums[-3] - nums[1]
        if nums[-2] - nums[2] < a:
            a = nums[-2] - nums[2]
        if nums[-1] - nums[3] < a:
            a = nums[-1] - nums[3]
        return a


class Solution:
    def reorderSpaces(self, text: str) -> str:
        words = [w for w in text.split(sep=' ') if w != ""]
        whiteSpaceCnt = sum(1 for x in text if x == ' ')

        avgWhileSpaceCnt = whiteSpaceCnt // (len(words) - 1)
        tailWhileSpace = whiteSpaceCnt % (len(words) - 1)

        return (' ' * avgWhileSpaceCnt).join(words) + (' ' * tailWhileSpace)


class Solution:
    twoDq = deque()
    threeDq = deque()
    fiveDq = deque()
    cur = 1
    total = 1
    twoDq.append(1)
    threeDq.append(1)
    threeDq.append(1)

    def __init__(self):
        pass

    def nthUglyNumber(self, n: int) -> int:
        while self.total < n:
            while self.twoDq[0] * 2 <= self.cur:
                self.twoDq.popleft()

            while self.threeDq[0] * 3 <= self.cur:
                self.threeDq.popleft()

            while self.fiveDq[0] * 5 <= self.cur:
                self.fiveDq.popleft()

            newCur = self.twoDq[0] * 2
            if self.threeDq[0] * 3 < newCur:
                newCur = self.threeDq[0] * 3

            if self.fiveDq[0] * 5 < newCur:
                newCur = self.fiveDq[0] * 5

            self.total += 1
            self.twoDq.append(newCur)
            self.threeDq.append(newCur)
            self.fiveDq.append(newCur)

            self.total += 1
            self.cur = newCur

        return self.cur


class _strRevCmp:
    __slots__ = {"__str"}

    def __init__(self, s: str):
        self.__str = s

    def __lt__(self, other: str):
        return other < self.__str


class Solution:
    def findKthNumber(self, n: int, k: int) -> int:
        return int(sorted([str(x) for x in range(1, n + 1)])[k])


class Solution:
    def partition(self, head: ListNode, x: int) -> ListNode:
        if not head: return None
        a = (e for e in self.traverseList(head) if e.val < x)
        b = (e for e in self.traverseList(head) if e.val >= x)
        c = self.merge(a, b)

        newHead = next(c)
        cur = newHead
        for e in c:
            cur.next = e
            cur = cur.next

        return newHead

    def merge(self, a: Iterable, b: Iterable):
        yield from a
        yield from b

    def traverseList(self, head: ListNode):
        while head is not None:
            yield head
            head = head.next


class Solution:
    def check(self, nums: List[int]) -> bool:
        revCnt = sum(1 if nums[i] - nums[i - 1] < 0 else 0 for i in range(1, len(nums)))

        return revCnt == 1 and nums[-1] <= nums[0] or revCnt == 0


class Solution:
    def canPermutePalindrome(self, s: str) -> bool:
        a = Counter(s)

        return len([x for x, i in a.items() if i % 2 == 1]) <= 1


class Solution:
    def printVertically(self, s: str) -> List[str]:
        words = re.split(r'\s+', s)
        maxLen = max(len(w) for w in words)

        res = []
        for i in range(0, maxLen):
            a = ''.join(' ' if i >= len(w) else w[i] for w in words)
            res.append(a.rstrip())

        return res


class Solution:
    def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
        arr = sorted(arr)
        minDiff = min(arr[i] - arr[i - 1] for i in range(1, len(arr) + 1))

        return [[arr[i - 1], arr[i]] for i in range(1, len(arr) + 1) if arr[i] - arr[i - 1] == minDiff]


class Solution:
    def countNodes(self, root: TreeNode) -> int:
        return self.preorder(root)

    def preorder(self, root: TreeNode) -> int:
        if root is None: return 0
        return 1 + self.preorder(root.left) + self.preorder(root.right)


class Solution:
    def mySqrt(self, x: int) -> int:
        return int(sqrt(x))


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        ctr = Counter(nums)

        a = [x for x, i in ctr if i == 1]

        return a[0]


class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        cache = set(x for x in nums if x > 0)
        maxVal = max(x for x in nums if x > 0)

        for i in range(1, maxVal + 1):
            if i not in cache:
                return i

        return maxVal + 1


class Solution:
    def maximumGap(self, nums: List[int]) -> int:
        nums = sorted(nums)

        a = (nums[i] - nums[i - 1] for i in range(1, len(nums)))

        return max(a)


class Solution:
    def canJump(self, nums: List[int]) -> bool:
        pass

    def canJMP(self, nums: list, cur: int, target: int):
        if cur >= target: return True
        for i in range(1, nums[cur]):
            if self.canJMP(nums, cur + i, target):
                return True

        return False


class Solution:
    def diameterOfBinaryTree(self, root: TreeNode) -> int:
        if root is None: return 0
        a = self.diameterOfBinaryTree(root.left)
        b = self.diameterOfBinaryTree(root.right)
        c = self.depth(root.left) + self.depth(root.right) + 1

        return max(a, b, c) - 1

    def depth(self, root: TreeNode):
        if root is None:
            return 0
        else:
            a = self.depth(root.left)
            b = self.depth(root.right)
            return a + 1 if a > b else b + 1


class Solution:
    def isStraight(self, nums: List[int]) -> bool:
        zeroCnt = sum(1 for x in nums if x == 0)
        start = min(x for x in nums if x != 0)
        end = max(x for x in nums if x != 0)

        for num, cnt in Counter(nums).items():
            if num != 0 and cnt > 1: return False

        return (end - start + 1) <= 5


class Solution:
    def smallestDistancePair(self, nums: List[int], k: int) -> int:
        hp = Heap([], lambda x: -x)
        for i in range(0, len(nums) - 1):
            for j in range(i + 1, len(nums)):
                if len(hp) < k:
                    hp.push(abs(nums[i] - nums[j]))
                elif abs(nums[i] - nums[j]) < hp.top():
                    hp.pop()
                    hp.push(abs(nums[i] - nums[j]))

        return hp.pop()


class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        stack = deque()
        res = [0]
        self.inorder(root, stack, re)
        return res[0]

    def inorder(self, root: TreeNode, stack: deque, res: List):
        if root is None: return
        if len(stack) == 0 or stack[-1] <= root.val:
            stack.append(root.val)
        if root.val < stack[-1]:
            res[0] += 1
        self.inorder(root.left, stack, res)
        self.inorder(root.right, stack, res)
        if root.val == stack[-1]:
            stack.pop()


class Solution:
    def equationsPossible(self, equations: List[str]) -> bool:
        eqs = (x for x in equations if x[1] == '=')
        neqs = (x for x in equations if x[1] == '!')

        ufs = UnionFindSet()
        for x in eqs:
            ufs.connect(x[0], x[3])

        for x in neqs:
            if ufs.isConnected(x[0], x[3]):
                return False

        return True


class Solution:
    def integerReplacement(self, n: int) -> int:
        if n == 1: return 0
        if n % 2 == 0: return 1 + self.integerReplacement(n // 2)
        a = 1 + self.integerReplacement(n - 1)
        b = 1 + self.integerReplacement(n + 1)
        return a if a < b else b


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        rudu = dict()
        for x in prerequisites:
            rudu[x[0]] = rudu.setdefault(x[0], 0) + 1

        pres = {x[1]: x[0] for x in prerequisites}

        ruduzero = set(x[1] for x in prerequisites if x[1] not in rudu)

        while len(ruduzero) > 0:
            newRuduZero = set()
            for x in ruduzero:
                if rudu[pres[x]] > 0:
                    rudu[pres[x]] -= 1
                if rudu[pres[x]] == 0:
                    newRuduZero.add(pres[x])

            ruduzero = newRuduZero

        return sum(v for k, v in rudu) == 0


class Solution:
    def constructArr(self, a: List[int]) -> List[int]:
        pre = [1] * len(a)
        for i in range(1, len(a)):
            pre[i] = pre[i - 1] * a[i - 1]

        post = [1] * len(a)
        for i in range(len(a) - 2, -1, -1):
            post[i] = post[i + 1] * a[i + 1]

        return [x * y for x, y in zip(pre, post)]


class Solution:
    def minOperations(self, nums: List[int], x: int) -> int:
        return self.minOp(nums, 0, len(nums), x)

    def minOp(self, nums: List[int], lo: int, hi: int, target: int) -> int:
        if target == 0: return 0
        if target < 0: return len(nums)
        a = 1 + self.minOp(nums, lo + 1, hi, target - nums[lo])
        b = 1 + self.minOp(nums, lo, hi - 1, target - nums[hi - 1])
        return min(a, b)


class Solution:
    def hasGroupsSizeX(self, deck: List[int]) -> bool:
        a = Counter(deck)
        if len(a) <= 1: return False

        cache = set()
        for x in a.values():
            if x <= 1: return False
            cache.add(x)

        return len(cache) == 1


class Solution:
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:
        a = sorted(intervals, key=lambda x: (x[0], -x[1]))
        pos = 0
        for i in range(1, len(a)):
            if a[i][0] >= a[pos][0] and a[i][1] <= a[pos][1]:
                continue
            else:
                pos += 1
                a[pos] = a[i]

        return pos + 1


class Solution:
    def widthOfBinaryTree(self, root: TreeNode) -> int:
        cache = dict()
        for (level, lohi) in self.inorder(root, 0, 0):
            if level in cache:
                if lohi < cache[level][0]:
                    cache[level][0] = lohi
                elif lohi > cache[level][1]:
                    cache[level][1] = lohi
            else:
                cache[level] = [lohi, lohi]

        return max(y - x + 1 for x, y in cache.values())

    def inorder(self, root: TreeNode, level: int, lohi: int):
        yield (level, lohi)
        if root.left is not None:
            yield from self.inorder(root.left, level + 1, lohi * 2)
        if root.right is not None:
            yield from self.inorder(root.right, level + 1, lohi * 2 + 1)


class Solution:
    def countPrimes(self, n: int) -> int:
        return sum(1 for x in range(2, n + 1) if isPrime(x))


class Solution:
    def deleteDuplicates(self, head):
        return self.deleteDup(head)

    def deleteDup(self, head: ListNode) -> ListNode:
        if head is None: return None
        if head.next is None:
            return head
        if head.val == head.next.val:
            return self.deleteDup(head.next)
        else:
            head.next = self.deleteDup(head.next)
            return head


class Solution:
    def deleteDuplicates(self, head: ListNode) -> ListNode:
        return self.deleteDup(head, set())

    def deleteDup(self, head: ListNode, cache: Set) -> ListNode:
        if head is None: return None
        if head.val in cache: return self.deleteDup(head.next, cache)
        if head.next is None:
            return head
        if head.val == head.next.val:
            cache.add(head.val)
            return self.deleteDup(head.next)
        else:
            head.next = self.deleteDup(head.next, cache)
            return head


class Solution:
    def getMinDistance(self, nums: List[int], target: int, start: int) -> int:
        cache: Dict[int, List[int]] = dict()
        for (i, num) in enumerate(nums):
            if num in cache:
                cache[num].append(i)
            else:
                cache[num] = [i]

        return min(cache[target], key=lambda x: abs(x - start))


class Solution:
    """
    @param a: the array a
    @return: return the index of median
    """

    def getAns(self, a):
        # write your code here
        b = sorted((x, i) for i, x in enumerate(a))
        return b[len(b) / 2][1]


class Solution:
    """
    @param m: the limit
    @param k: the sum of choose
    @param arr: the array
    @return: yes or no
    """

    def depress(self, m, k, arr: List[int]):
        # Write your code here.
        arr.sort()
        i = 0
        res = 0
        for youyu in arr:
            res += youyu
            i += 1
            if i == k:
                break

        if res >= m:
            return 'yes'
        else:
            return 'no'


class Solution:
    """
    @param nums: an array of integers
    @return: the number of unique integers
    """

    def deduplication(self, nums):
        # write your code here
        cache = set()
        for n in nums:
            cache.add(n)

        i = 0
        for n in cache:
            nums[i] = n
            i += 1

        return i


class Solution:
    """
    @param str: The identifier need to be judged.
    @return: Return if str is a legal identifier.
    """

    def isLegalIdentifier(self, str):
        # Write your code here.
        return re.search(r'[^0-9][a-zA-Z0-9]*', str) is not None


class Solution:
    """
    @param A: The A
    @param B: The B
    @return: Returns the sum of all qualified numbers
    """

    def getSum(self, A, B):
        # Write your code here
        return sum(x for x in range(A, B + 1) if x % 3 == 0)


class Solution:
    def levelOrder(self, root: 'Node') -> List[List[int]]:
        res: List[List[int]] = []
        if root == None: return res

        curList: List[int] = []
        curLevel = 0
        for (node, level) in self.levelOrder(root):
            if curLevel == level:
                curList.append(node.val)
            else:
                res.append(curList)
                curList = [node.val]
                curLevel = level

        return res

    def levelOrderTraverse(self, root: Node):
        if root != None:
            queue: deque[Tuple[Node, int]] = deque()
            queue.append((root, 0))
            while len(queue) > 0:
                (curNode, curLevel) = queue.popleft()
                yield (curNode, curLevel)
                if curNode.children == None:
                    continue
                for node in curNode.children:
                    if node == None:
                        continue
                    queue.append((node, curLevel + 1))
