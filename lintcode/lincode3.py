from collections import Counter


class Solution:
    """
    @param k: An integer
    @param n: An integer
    @return: An integer denote the count of digit k in 1..n
    """

    def digitCounts(self, k, n):
        # write your code here
        res = 0
        for i in range(n + 1):
            for d in self.digits(i):
                if d == k:
                    res += 1

        return res

    def digits(self, n):
        res = []
        while n > 0:
            res.append(n % 10)
            n //= 10

        return res


if __name__ == '__main__':
    a = Solution().digitCounts(3, 12)
    print(a)
