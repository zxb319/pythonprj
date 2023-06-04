
class TTT:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type,exc_val,exc_tb)


if __name__ == '__main__':
    t=TTT()
    with t:
        print(1/0)
