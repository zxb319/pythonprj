from typing import List
import heapq


class Solution:
    def __init__(self):
        self._pq = []
        heapq.heappush(self._pq, 1)
        self._cache=set()

    def nthSuperUglyNumber(self, n: int, primes: List[int]) -> int:
        if n == 1:
            return heapq.heappop(self._pq)
        else:
            cur = heapq.heappop(self._pq)
            for p in primes:
                curp=cur*p
                if curp in self._cache:
                    continue
                heapq.heappush(self._pq, curp)
                self._cache.add(curp)

            return self.nthSuperUglyNumber(n - 1, primes)


if __name__ == '__main__':
    s = Solution()
    res = s.nthSuperUglyNumber(12, [2, 7, 13, 19])
    print(res)
