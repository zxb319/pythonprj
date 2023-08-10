import math
from typing import List


class Solution:
    cache={}
    def minDistance(self, word1: str, word2: str) -> int:
        k=(word1,word2)
        if k in Solution.cache:
            return Solution.cache[k]
        if not word1:
            return len(word2)
        if not word2:
            return len(word1)
        if word1[0] == word2[0]:
            return self.minDistance(word1[1:], word2[1:])

        a = self.minDistance(word1, word2[1:]) + 1
        b = self.minDistance(word1[1:], word2) + 1
        r=min(a,b)
        Solution.cache[k]=r
        return r


if __name__ == '__main__':
    s = Solution()
    word1 = 'leetcode'
    word2 = 'etco'
    a = s.minDistance(word1, word2)
    print(a)
