import sys

# sys.path.append('..')

import heapq
import random
import re
from functools import cmp_to_key
from typing import List, Optional
from collections import Counter, deque
from math import sqrt
from random import randint
from collections import OrderedDict

# from dsa.fraction import Fraction
from lintcode import *
from dsa.heap import Heap

class Solution:
    def editDistance(self , str1: str, str2: str) -> int:
        # write code here
        cache={}
        return self.edit_dist(str1,0,str2,0,cache)

    def edit_dist(self,str1:str,idx1:int,str2:str,idx2:int,cache:dict):
        if (idx1,idx2) in cache:
            return cache[(idx1,idx2)]
        if idx1>=len(str1):
            return len(str2)-idx2
        if idx2>=len(str2):
            return len(str1)-idx1

        if str1[idx1]==str2[idx2]:
            return self.edit_dist(str1,idx1+1,str2,idx2+1)

        else:
            res1=self.edit_dist(str1,idx1,str2,idx2+1,cache)
            res2=self.edit_dist(str1,idx1+1,str2,idx2,cache)
            res3=self.edit_dist(str1,idx1+1,str2,idx2+1,cache)
            res=min(res1,res2,res3)+1
            cache[(idx1,idx2)]=res
            return res

class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        graph={}
        for i,e in enumerate(equations):
            if e[0] in graph:
                graph[e[0]][e[1]]=values[i]
            else:
                graph[e[0]]={e[1]:values[i]}

            if e[1] in graph:
                graph[e[1]][e[0]] = 1/values[i]
            else:
                graph[e[1]] = {e[0]: 1/values[i]}
        res=[]
        for query in queries:
            res.append(self.answer_query(graph,query[0],query[1],1))

        return res

    def answer_query(self,graph:dict,from_:str,to:str,cur:float):
        if from_ not in graph:
            return -1
        if from_==to:
            return cur
        for mi,v in graph[from_].items():
            rest=self.answer_query(graph,mi,to,cur*v)
            if rest!=-1:
                return rest

        return -1

class Solution:
    def __init__(self):
        self._cache={}
    def uniquePaths(self, m: int, n: int) -> int:
        if (m,n) in self._cache:
            return self._cache[(m,n)]
        if m==0 and n==0:
            return 0
        elif m==0 or n==0:
            return 1
        res=self.uniquePaths(m-1,n)+self.uniquePaths(m,n-1)
        self._cache[(m,n)]=res
        return res

class Solution:
    def __init__(self):
        self._cache = {}

    def jump(self, nums: List[int]) -> int:
        return self.do_jump(nums, 0, len(nums))

    def do_jump(self, nums: List, lo: int, hi: int):
        if (lo, hi) in self._cache:
            return self._cache[(lo, hi)]
        if hi <= lo:
            return 0
        res = hi - lo
        for i in range(1, nums[lo] + 1):
            cur = 1 + self.do_jump(nums, lo + i, hi)
            if res < cur:
                res = cur
        self._cache[(lo, hi)] = res
        return res


class Solution:
    def constructMaximumBinaryTree(self, nums: List[int]) -> TreeNode:
        return self.con(nums, 0, len(nums))

    def con(self, nums: List, lo: int, hi: int):
        if hi <= lo:
            return None
        index, val = max(((i, nums[i]) for i in range(lo, hi)), key=lambda x: x[1])
        left = self.con(nums, lo, index)
        right = self.con(nums, index + 1, hi)
        return TreeNode(val, left, right)


class Solution:
    def lenLongestFibSubseq(self, arr: List[int]) -> int:
        cache = []
        return self.longest_fib(arr, cache)

    def longest_fib(self, arr: List[int], cache: List):
        for a in arr:
            cur = []
            for seq in cache:
                if len(seq) >= 2 and seq[-1] + seq[-2] == a:
                    cur.append(seq + [a])
                else:
                    cur.append([seq[-1], a])

            cur.append([a])
            cache.append(cur)

        res = max(cache, key=lambda x: len(x))
        return 0 if len(res) <= 2 else len(res)


class Solution:
    def maxProduct(self, root: Optional[TreeNode]) -> int:
        total_sum = self.sum(root)
        res = 0

        def max_product(root: TreeNode):
            nonlocal res
            for node in self.mid_order(root):
                left_sum = self.sum(node.left)
                right_sum = self.sum(node.right)
                cur = max(left_sum * (total_sum - left_sum), right_sum * (total_sum - right_sum))
                if res < cur:
                    res = cur

        max_product(root)
        return res % (10 ** 9 + 7)

    def mid_order(self, root: TreeNode):
        if root:
            yield from self.mid_order(root.left)
            yield root
            yield from self.mid_order(root.right)

    def sum(self, root: TreeNode):
        if hasattr(root, 'sum'):
            return root.sum

        if not root:
            return 0

        res = root.val + self.sum(root.left) + self.sum(root.right)
        root.sum = res
        return res
