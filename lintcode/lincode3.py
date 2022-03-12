from collections import Counter
from typing import List


def max_profit(prices: List[float], fee: float):
    status = {
        0: 0,
        1: -prices[0]
    }

    for i in range(1, len(prices)):
        cur = {}
        for c, p in status.items():
            if c == 0:
                cur[1] = max(p - prices[i], status[1])
            elif c == 1:
                cur[0] = max(p + prices[i] - fee, status[0])

        status = cur

    return status[0]


if __name__ == '__main__':
    a = max_profit([1, 3, 2, 8, 4, 9], 2)
    print(a)
