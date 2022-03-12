import threading


class LockGuard:
    __slots__ = {"__lock"}

    def __init__(self, lock: threading.Lock):
        self.__lock = lock

    def __enter__(self):
        self.__lock.acquire(True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__lock.release()
