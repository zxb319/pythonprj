import math
import random
from typing import List, Tuple, Union


class Vector:
    def __init__(self, items: list):
        if len(items) == 0:
            raise ArithmeticError(rf'dim of vector bigger than zero!')
        self.items = items

    def __mul__(self, other: Union[int, float]):
        return Vector([other * x for x in self.items])

    def __rmul__(self, other: Union[int, float]):
        return self * other

    def __add__(self, other: 'Vector'):
        self.assert_lengths_match(self, other)
        return Vector([x + y for x, y in zip(self.items, other.items)])

    def dot_mul(self, other: 'Vector'):
        self.assert_lengths_match(self, other)
        return sum(x * y for x, y in zip(self.items, other.items))

    def cross_mul(self, other: 'Vector'):
        self.assert_lengths_match(self, other)
        self.assert_length([2, 3])
        if self.dim == 2:
            return Vector([0, 0, self.items[0] * other.items[1] - self.items[1] * other.items[0]])
        else:
            return Vector([
                self.items[1] * other.items[2] - self.items[2] * other.items[1],
                self.items[2] * other.items[0] - self.items[0] * other.items[2],
                self.items[0] * other.items[1] - self.items[1] * other.items[0],
            ])

    def __str__(self):
        return rf'[{" ".join(str(x) for x in self.items)}]'

    @property
    def dim(self):
        return len(self.items)

    @property
    def length(self):
        return sum([x * x for x in self.items]) ** 0.5

    def assert_length(self, lengths: list):
        if self.dim not in lengths:
            raise ArithmeticError(rf'vector length is not in {lengths}!')

    @classmethod
    def assert_lengths_match(cls, v1: 'Vector', v2: 'Vector'):
        if len(v1.items) != len(v2.items):
            raise ArithmeticError(rf'two vector lengths are not match!')

    @classmethod
    def arc(cls, v1: 'Vector', v2: 'Vector'):
        return math.acos(v1.dot_mul(v2) / v1.length / v2.length)


class Matrix:
    def __init__(self, elems: List[List]):
        if not elems or not elems[0]:
            raise ArithmeticError(rf'matrix dim must not be zero!')
        self._elems = elems

    @property
    def form(self):
        return len(self._elems), len(self._elems[0])

    def assert_same_form(self, other: 'Matrix'):
        if self.form != other.form:
            raise ArithmeticError(rf'two matrices form must be same!')

    def assert_dotable(self, other: 'Matrix'):
        if self.form[1] != other.form[0]:
            raise ArithmeticError(rf'two matrices are not dotable!')

    def assert_squared(self):
        form = self.form
        if form[0] != form[1]:
            raise ArithmeticError(rf'matrix is not squared!')

    def __mul__(self, c: Union[int, float, 'Matrix']):
        if isinstance(self, Matrix):
            return self.dot(c)
        ret = []
        for row in self._elems:
            ret.append([c * x for x in row])
        return Matrix(ret)

    def __rmul__(self, other: Union[int, float, 'Matrix']):
        if isinstance(self, Matrix):
            return other.dot(self)
        return self * other

    def __add__(self, other: 'Matrix'):
        self.assert_same_form(other)
        ret = []
        for arow, brow in zip(self._elems, other._elems):
            ret.append([a + b for a, b in zip(arow, brow)])

        return Matrix(ret)

    def __sub__(self, other: 'Matrix'):
        self.assert_same_form(other)
        ret = []
        for arow, brow in zip(self._elems, other._elems):
            ret.append([a - b for a, b in zip(arow, brow)])

        return Matrix(ret)

    def dot(self, other: 'Matrix'):
        self.assert_dotable(other)
        ret = []
        for arow in self._elems:
            cur_row = [0] * other.form[1]
            for aitm, brow in zip(arow, other._elems):
                cur = [aitm * bitm for bitm in brow]
                cur_row = [a + b for a, b in zip(cur_row, cur)]
            ret.append(cur_row)

        return Matrix(ret)

    def __str__(self):
        ret = []
        for r in self._elems:
            ret.append(' '.join(rf'({round(x, 2)})' for x in r))
        s = '\n'.join(ret)
        return f"[Matrix\n{s}\n]"

    @classmethod
    def identity(cls, n):
        ret = [[0] * n for i in range(n)]
        for i in range(len(ret)):
            ret[i][i] = 1

        return Matrix(ret)

    def __make_sure_pivot(self, items: List[List], k: int, ret: List[List]):
        if items[k][k] == 0:
            exchanged = False
            for i in range(k + 1, len(items)):
                if items[i][k] != 0:
                    exchanged = True
                    items[i], items[k] = items[k], items[i]
                    ret[i], ret[k] = ret[k], ret[i]
                    break
            if not exchanged:
                raise ArithmeticError(rf'cannot inverse the matrix!')
        if items[k][k] != 1:
            ret[k] = [v / items[k][k] for v in ret[k]]
            items[k] = [v / items[k][k] for v in items[k]]

    @property
    def inverse(self):
        self.assert_squared()
        ret = [[v for v in row] for row in self._elems]
        r = self.identity(len(ret))

        for c in range(0, len(ret)):
            self.__make_sure_pivot(ret, c, r._elems)
            for i in range(c + 1, len(ret)):
                f = -ret[i][c] / ret[c][c]
                ret[i] = [v + f * last_v for v, last_v in zip(ret[i], ret[c])]
                r._elems[i] = [v + f * last_v for v, last_v in zip(r._elems[i], r._elems[c])]

        for c in range(len(ret) - 1, -1, -1):
            for i in range(c - 1, -1, -1):
                f = -ret[i][c] / ret[c][c]
                ret[i] = [v + f * last_v for v, last_v in zip(ret[i], ret[c])]
                r._elems[i] = [v + f * last_v for v, last_v in zip(r._elems[i], r._elems[c])]

        return r


if __name__ == '__main__':
    a = Matrix([
        [1, 1, ],
        [4, 2, ],
    ])

    N = 2
    a = []
    for i in range(N):
        a.append([random.random()*2 for j in range(N)])
    a = Matrix(a)

    from dsa.run_time import CostTime

    with CostTime():
        ai = a.inverse

    print(ai)
    print(a)
    print(a * ai)

    # print(a.inverse*Matrix([
    #     [15],
    #     [52],
    # ]))
