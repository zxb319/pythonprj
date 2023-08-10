import enum
import re
from typing import List, Tuple


class Token:
    class Type(enum.Enum):
        IDN = 1
        INT = 2
        FLOAT = 3
        STR = 4

        ADD = 5
        SUB = 6
        MUL = 7
        DIV = 8
        POW = 9

        EQ = 10
        NE = 11
        LT = 12
        LE = 13
        GT = 14
        GE = 15
        IN = 16
        BETWEEN = 17

        NOT = 18
        AND = 19
        OR = 20

        LP = 21
        RP = 22
        LZ = 23
        RZ = 24
        LD = 25
        RD = 26

        WHITE = 27

        COMMA = 28

    TOKEN_TYPE_REGS = [
        (Type.IN, r'\bin\b'),
        (Type.BETWEEN, r'\bbetween\b'),

        (Type.NOT, r'\bnot\b'),
        (Type.AND, r'\band\b'),
        (Type.OR, r'\bor\b'),

        (Type.IDN, r'[a-z_][a-z\d_]*'),
        (Type.INT, r'[\+\-]?\d+'),
        (Type.FLOAT, r'[\+\-]?(\d+\.\d*|\.\d+)(e[\+\-]?\d+)?'),
        (Type.STR, r'''(\"(\\\"|[^\"])*\"|\'(\\\'|[^\'])*\')'''),

        (Type.ADD, r'\+'),
        (Type.SUB, r'\-'),
        (Type.POW, r'\*\*'),
        (Type.MUL, r'\*'),
        (Type.DIV, r'/'),

        (Type.EQ, r'=='),
        (Type.NE, r'<>'),
        (Type.LE, r'<='),
        (Type.LT, r'<'),
        (Type.GE, r'>='),
        (Type.GT, r'>'),

        (Type.LP, r'\('),
        (Type.RP, r'\)'),
        (Type.LZ, r'\['),
        (Type.RZ, r'\]'),
        (Type.LD, r'\{'),
        (Type.RD, r'\}'),
        (Type.COMMA, r','),

        (Type.WHITE, r'\s+'),
    ]

    TOKEN_TYPE_REGS: List[Tuple[Type, re.Pattern]] = [(t, re.compile(r, re.IGNORECASE)) for t, r in TOKEN_TYPE_REGS]

    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return rf'<{self.type}, `{self.value}`>'


def get_tokens(s: str):
    ret = []
    cp = 0
    while cp < len(s):
        found = False
        for t, r in Token.TOKEN_TYPE_REGS:
            match = r.match(s, cp)
            if match:
                found = True
                if t != Token.Type.WHITE:
                    ret.append(Token(t, match.group(0)))
                cp += len(match.group(0))

        if not found:
            raise Exception(rf'token not recognized near: {s[cp:cp + 100]}')

    return ret


class Integer:
    def __init__(self, value):
        self.value = int(value)


class Float:
    def __init__(self, value):
        self.value = float(value)


class String:
    def __init__(self, value):
        self.value = value


class Array:
    def __init__(self, exprs: List):
        self.exprs = exprs

    @property
    def value(self):
        return [x.value for x in self.exprs]


class Set:
    def __init__(self, exprs: List):
        self.exprs = exprs

    @property
    def value(self):
        return {x.value for x in self.exprs}


class Dictionary:
    def __init__(self, exprs: List):
        self.exprs = exprs

    @property
    def value(self):
        return {x.value: y.value for x, y in self.exprs}


class Function:
    def __init__(self, func_name, func_map: dict, *args, **kwargs):
        if func_name not in func_map:
            raise fr'function:{func_name} not defined!'

        self.func = func_map[func_name]
        self.args = args
        self.kwargs = kwargs

    @property
    def value(self):
        return self.func(*self.args, **self.kwargs)


class BinaryOperatorExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Power(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value ** self.right.value


class Multiply(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value * self.right.value


class Divide(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value / self.right.value


class Negative:
    def __init__(self, expr):
        self.expr = expr

    @property
    def value(self):
        return -self.expr.value


class Add(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value + self.right.value


class Subtract(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value - self.right.value


class Less(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value < self.right.value


class LessEqual(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value <= self.right.value


class Greater(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value > self.right.value


class GreaterEqual(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value >= self.right.value


class Equal(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value == self.right.value


class NotEqual(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value != self.right.value


class In(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value in self.right.value


class Between:
    def __init__(self, left, middle, right):
        self.left = left
        self.middle = middle
        self.right = right

    @property
    def value(self):
        return self.middle.value <= self.left.value <= self.right.value


class Not:
    def __init__(self, expr):
        self.expr = expr

    @property
    def value(self):
        return not self.expr.value


class And(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value and self.right.value


class Or(BinaryOperatorExpression):
    @property
    def value(self):
        return self.left.value or self.right.value


class Agent:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.cp = 0

    def syntax_error(self):
        return Exception(rf'syntax error near: {self.cp} !')

    def get_integer(self):
        ret = Integer(self.tokens[self.cp].value)
        self.cp += 1
        return ret

    def get_float(self):
        ret = Float(self.tokens[self.cp].value)
        self.cp += 1
        return ret

    def get_string(self):
        ret = String(self.tokens[self.cp].value)
        self.cp += 1
        return ret

    def get_parenthesised_expr(self):
        ret = self.get_assign_expr()
        if self.tokens[self.cp].type == Token.Type.RP:
            self.cp += 1
        else:
            raise self.syntax_error()
        return ret

    def get_atomic_expr(self):
        cur_token = self.tokens[self.cp]
        if cur_token.type == Token.Type.INT:
            return self.get_integer()
        elif cur_token.type == Token.Type.FLOAT:
            return self.get_float()
        elif cur_token.type == Token.Type.STR:
            return self.get_string()
        elif cur_token.type == Token.Type.LP:
            return self.get_parenthesised_expr()
        else:
            raise self.syntax_error()

    def get_power_expr(self):
        ret = []
        while True:
            ret.append(self.get_atomic_expr())
            if self.cp < len(self.tokens) and self.tokens[self.cp].type == Token.Type.POW:
                self.cp += 1
            else:
                break

        if len(ret) == 1:
            return ret[0]

        expr = ret[-1]
        for i in range(len(ret) - 2, -1, -1):
            expr = Power(ret[i], expr)

        return expr

    def get_multiply_expr(self):
        if self.tokens[self.cp].type in (Token.Type.ADD,):
            self.cp += 1
            return self.get_power_expr()
        elif self.tokens[self.cp].type in (Token.Type.SUB,):
            self.cp += 1
            return Negative(self.get_power_expr())

        ret = None
        cur_expr_type = None
        while True:
            if not ret:
                ret = self.get_power_expr()
            else:
                ret = cur_expr_type(ret, self.get_power_expr())
            if self.cp < len(self.tokens) and self.tokens[self.cp].type == Token.Type.MUL:
                self.cp += 1
                cur_expr_type = Multiply
            elif self.cp < len(self.tokens) and self.tokens[self.cp].type == Token.Type.DIV:
                self.cp += 1
                cur_expr_type = Divide
            else:
                break
        return ret

    def get_add_expr(self):
        ret = None
        cur_expr_type = None
        while True:
            if not ret:
                ret = self.get_multiply_expr()
            else:
                ret = cur_expr_type(ret, self.get_multiply_expr())
            if self.cp < len(self.tokens) and self.tokens[self.cp].type == Token.Type.ADD:
                self.cp += 1
                cur_expr_type = Add
            elif self.cp < len(self.tokens) and self.tokens[self.cp].type == Token.Type.SUB:
                self.cp += 1
                cur_expr_type = Subtract
            else:
                break
        return ret

    def get_cmp_expr(self):
        left=self.get_add_expr()
        cur_token=self.tokens[self.cp]
        if cur_token.type==Token.Type.EQ:
            expr_type=Equal
        elif cur_token.type==Token.Type.NE:
            expr_type=NotEqual
        elif cur_token.

    def get_not_expr(self):
        pass

    def get_and_expr(self):
        pass

    def get_or_expr(self):
        pass

    def get_assign_expr(self):
        pass

    def get_if_expr(self):
        pass

    def get_while_expr(self):
        pass

    def get_for_expr(self):
        pass

    def get_function_define(self):
        pass


if __name__ == '__main__':
    s = 'func   (  1   +   2,  "w w\'w")'
    tokens = get_tokens(s)
    print(*tokens, sep='  ')
