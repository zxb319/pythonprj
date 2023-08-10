import random
from collections import deque


def find_unique(nums: list):
    a = 0
    b = 0
    for c in nums:
        d = ~a & b & c | a & ~b & ~c
        e = ~a & ~b & c | ~a & b & ~c
        a = d
        b = e

    return b


if __name__ == '__main__':
    nums = deque()
    have_select = False
    for i in range(100):
        n = random.randint(0, 100)
        is_tail = random.random()

        if is_tail < 0.5:
            for k in range(3):
                nums.append(n)
        else:
            for k in range(3):
                nums.appendleft(n)

        selected = random.random()
        if not have_select and selected > 0.5:
            have_select = True
            is_tail = random.random()
            n += 97
            if is_tail < 0.5:
                nums.append(n)

            else:
                nums.appendleft(n)

            print(n)

    print(find_unique(nums))
