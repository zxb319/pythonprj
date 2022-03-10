from typing import List


class Matrix:
    def __init__(self, elems: List[List[float]]):
        self._elems = elems

    def __mul__(self, other: "Matrix"):
        assert len(self._elems[0]) == len(other._elems)

        res = []
        for i in range(len(self._elems)):
            r = []
            for j in range(len(other._elems[0])):
                cur = sum(self._elems[i][k] * other._elems[k][j] for k in range(len(self._elems[0])))
                r.append(cur)

            res.append(r)

        return Matrix(res)

    @property
    def t(self):
        res = []
        for j in range(len(self._elems[0])):
            res.append([self._elems[i][j] for i in range(len(self._elems))])

        return Matrix(res)

    def __str__(self):
        res = [str(r) for r in self._elems]

        return '\n'.join(res)


if __name__ == '__main__':
    m = Matrix([
        [1, 2],
        [3, 4],
        [5, 6]
    ])

    print(m)
    print(m.t)
