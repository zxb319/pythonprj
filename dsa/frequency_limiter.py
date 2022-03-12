import time
from typing import Callable

from dsa.fixed_len_queue import FixedLenQueue


def frequency_limit(secs: int, times: int):
    class FrequencyLimiter:
        def __init__(self, callable_object: Callable):
            self._callable_object = callable_object
            self._secs = secs
            self._times = times
            self._recent_called_times = FixedLenQueue(self._times)

        def __call__(self, *args, **kwargs):
            while len(
                    self._recent_called_times) == self._times and self._recent_called_times.head() + self._secs >= time.time():
                time.sleep(1)

            res = self._callable_object(*args, **kwargs)
            self._recent_called_times.append(time.time())
            return res

    return FrequencyLimiter


if __name__ == '__main__':
    @frequency_limit(5, 10)
    def test():
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        return time.time()


    for i in range(40):
        a=test()
        print(a)
