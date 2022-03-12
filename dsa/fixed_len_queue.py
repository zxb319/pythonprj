from collections import deque
from typing import Any


class FixedLenQueue:
    def __init__(self, l: int):
        self._l = l
        self._q = deque()

    def append(self, val: Any):
        if len(self._q) == self._l:
            self._q.popleft()
        self._q.append(val)

    def popleft(self):
        return self._q.popleft()

    def __len__(self):
        return len(self._q)

    def head(self):
        return self._q[0]

    def tail(self):
        return self._q[-1]