import enum
import re
from typing import List


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return rf'<{self.type} {self.value}>'

    def __repr__(self):
        return self.__str__()

    class Type(enum.Enum):
        IDN = 1

        INT = 2
        FLOAT = 3
        STR = 4

        ADD = 5
        SUB = 6
        MUL = 7
        DIV = 8
        FLOOR_DIV = 9
        MOD = 10
        POW = 11

        EQ = 12
        NE = 13
        GT = 14
        GE = 15
        LT = 16
        LE = 17

        LP = 18
        RP = 19
        LZ = 20
        RZ = 21
        LD = 22
        RD = 23

        ASSIGN = 24

        COMMA = 25
        COLON = 26
        POINT = 27
        AT = 28

        NOT = 29
        AND = 30
        OR = 31

        IF = 32
        ELIF = 33
        ELSE = 34

        WHILE = 35
        FOR = 36
        IN = 37

        WITH = 38
        AS = 39

        TRY = 40
        EXCEPT = 41
        FINALLY = 42

        COMMENT = 43
        WHITE = 44

        FROM = 45
        IMPORT = 46

        DEF = 47
        CLASS = 48

        BACK_SLASH = 49

        NONE = 50

        TRUE = 51
        FALSE = 52

    KEYs = {
        'not': Type.NOT,
        'and': Type.AND,
        'or': Type.OR,
        'if': Type.IF,
        'elif': Type.ELIF,
        'else': Type.ELSE,
        'while': Type.WHILE,
        'for': Type.FOR,
        'in': Type.IN,
        'with': Type.WITH,
        'as': Type.AS,
        'try': Type.TRY,
        'except': Type.EXCEPT,
        'finally': Type.FINALLY,
        'from': Type.FROM,
        'import': Type.IMPORT,
        'def': Type.DEF,
        'class': Type.CLASS,
        'None': Type.NONE,
        'True': Type.TRUE,
        'False': Type.FALSE,
    }

    REGs = [
        (Type.IDN, re.compile(r'[a-z_][a-z_0-9\.]*', re.IGNORECASE | re.S)),
        (Type.INT, re.compile(r'\d+', re.IGNORECASE | re.S)),
        (Type.FLOAT, re.compile(r'(\d+\.\d*|\.\d+)(e[\+\-]\d+)?', re.IGNORECASE | re.S)),
        (Type.STR, re.compile(r'''\'{3}((?!\'{3}).)*\'{3}''', re.IGNORECASE | re.S)),
        (Type.STR, re.compile(r'''\"{3}((?!\"{3}).)*\"{3}''', re.IGNORECASE | re.S)),
        (Type.STR, re.compile(r'''\'([^\']|\\\')*\'''', re.IGNORECASE | re.S)),
        (Type.STR, re.compile(r'''\"([^\"]|\\\")*\"''', re.IGNORECASE | re.S)),
        (Type.ADD, re.compile(r'\+', re.IGNORECASE | re.S)),
        (Type.SUB, re.compile(r'\-', re.IGNORECASE | re.S)),

        (Type.POW, re.compile(r'\*\*', re.IGNORECASE | re.S)),
        (Type.MUL, re.compile(r'\*', re.IGNORECASE | re.S)),

        (Type.FLOOR_DIV, re.compile(r'//', re.IGNORECASE | re.S)),
        (Type.DIV, re.compile(r'\/', re.IGNORECASE | re.S)),

        (Type.MOD, re.compile(r'%', re.IGNORECASE | re.S)),

        (Type.EQ, re.compile(r'\=\=', re.IGNORECASE | re.S)),
        (Type.ASSIGN, re.compile(r'=', re.IGNORECASE | re.S)),
        (Type.NE, re.compile(r'\!\=', re.IGNORECASE | re.S)),

        (Type.GE, re.compile(r'>=', re.IGNORECASE | re.S)),
        (Type.GT, re.compile(r'>', re.IGNORECASE | re.S)),
        (Type.LE, re.compile(r'<=', re.IGNORECASE | re.S)),
        (Type.LT, re.compile(r'<', re.IGNORECASE | re.S)),

        (Type.LP, re.compile(r'\(', re.IGNORECASE | re.S)),
        (Type.RP, re.compile(r'\)', re.IGNORECASE | re.S)),
        (Type.LZ, re.compile(r'\[', re.IGNORECASE | re.S)),
        (Type.RZ, re.compile(r'\]', re.IGNORECASE | re.S)),
        (Type.LD, re.compile(r'\{', re.IGNORECASE | re.S)),
        (Type.RD, re.compile(r'\}', re.IGNORECASE | re.S)),

        (Type.COMMA, re.compile(r'\,', re.IGNORECASE | re.S)),
        (Type.COLON, re.compile(r'\:', re.IGNORECASE | re.S)),
        (Type.POINT, re.compile(r'\.', re.IGNORECASE | re.S)),
        (Type.AT, re.compile(r'\@', re.IGNORECASE | re.S)),

        (Type.COMMENT, re.compile(r'\#[^\n]*', re.IGNORECASE | re.S)),
        (Type.WHITE, re.compile(r'\s+', re.IGNORECASE | re.S)),
        (Type.BACK_SLASH, re.compile(r'\\', re.IGNORECASE | re.S)),

    ]


def get_tokens(s: str):
    ret = []
    pos = 0
    while pos < len(s):
        found = False
        for reg in Token.REGs:
            t: Token.Type = reg[0]
            r: re.Pattern = reg[1]
            mat = r.match(s, pos)
            if mat:
                found = True
                val = mat.group(0)
                if t != Token.Type.WHITE:
                    if val in Token.KEYs:
                        ret.append(Token(Token.KEYs[val], val))
                    else:
                        ret.append(Token(t, val))
                pos += len(val)

        if not found:
            raise Exception(rf'无法识别的token:{s[pos:pos + 30]}')

    return ret


class ZInt:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class ZFloat:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class ZStr:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class ZIdn:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class ZIndexer:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return rf'{self.a}[{self.b}]'


class ZTuple:
    def __init__(self, values: List):
        self.values = values

    def __str__(self):
        return rf"({', '.join(str(x) for x in self.values)},)"


class ZList:
    def __init__(self, values: List):
        self.values = values

    def __str__(self):
        return rf"[{', '.join(str(x) for x in self.values)},]"


class ZSet:
    def __init__(self, values: List):
        self.values = values

    def __str__(self):
        body = ', '.join(str(x) for x in self.values)
        return '{' + body + ',}'


class ZKeyValuePair:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return rf'{self.key}: {self.value}'


class ZDict:
    def __init__(self, kv_pairs: List):
        self.kv_pairs = kv_pairs

    def __str__(self):
        body = ', '.join(str(x) for x in self.kv_pairs)
        return '{' + body + ',}'


class ZTrue:
    def __str__(self):
        return 'True'


class ZFalse:
    def __str__(self):
        return 'False'


class ZNone:
    def __str__(self):
        return 'None'


class ZPow:
    def __init__(self, b, p):
        self.base = b
        self.power = p

    def __str__(self):
        return rf'{self.base} ** {self.power}'


class ZMul:
    def __init__(self, a, b):
        self.left = a
        self.right = b

    def __str__(self):
        return rf'{self.left} * {self.right}'


class ZDiv:
    def __init__(self, a, b):
        self.left = a
        self.right = b

    def __str__(self):
        return rf'{self.left} / {self.right}'


class ZFloorDiv:
    def __init__(self, a, b):
        self.left = a
        self.right = b

    def __str__(self):
        return rf'{self.left} // {self.right}'


class ZMod:
    def __init__(self, a, b):
        self.left = a
        self.right = b

    def __str__(self):
        return rf'{self.left} % {self.right}'


class ZNeg:
    def __init__(self, a):
        self.a = a

    def __str__(self):
        return rf'-{self.a}'


class ZPos:
    def __init__(self, a):
        self.a = a

    def __str__(self):
        return rf'+{self.a}'


class ZAdd:
    def __init__(self, a, b):
        self.left = a
        self.right = b

    def __str__(self):
        return rf'{self.left} + {self.right}'


class ZSub:
    def __init__(self, a, b):
        self.left = a
        self.right = b

    def __str__(self):
        return rf'{self.left} - {self.right}'


class ZEq:
    def __init__(self, a, b):
        self.left = a
        self.right = b

    def __str__(self):
        return rf'{self.left} == {self.right}'


class ZNe:
    def __init__(self, a, b):
        self.left = a
        self.right = b

    def __str__(self):
        return rf'{self.left} != {self.right}'


class ZLt:
    def __init__(self, a, b):
        self.left = a
        self.right = b

    def __str__(self):
        return rf'{self.left} < {self.right}'


class ZLe:
    def __init__(self, a, b):
        self.left = a
        self.right = b

    def __str__(self):
        return rf'{self.left} <= {self.right}'


class ZGt:
    def __init__(self, a, b):
        self.left = a
        self.right = b

    def __str__(self):
        return rf'{self.left} > {self.right}'


class ZGe:
    def __init__(self, a, b):
        self.left = a
        self.right = b

    def __str__(self):
        return rf'{self.left} >= {self.right}'


class ZNot:
    def __init__(self, a):
        self.a = a

    def __str__(self):
        return rf'not {self.a}'


class ZAnd:
    def __init__(self, a, b):
        self.left = a
        self.right = b

    def __str__(self):
        return rf'{self.left} and {self.right}'


class ZOr:
    def __init__(self, a, b):
        self.left = a
        self.right = b

    def __str__(self):
        return rf'{self.left} or {self.right}'


class ZParExpr:
    def __init__(self, a):
        self.a = a

    def __str__(self):
        return rf'({self.a})'


class SyntaxAgent:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def assert_not_end(self):
        if self.pos >= len(self.tokens):
            raise Exception(rf'syntax error : eof!')

    def get_factor(self):
        self.assert_not_end()
        cur_token = self.tokens[self.pos]
        if cur_token.type == Token.Type.INT:
            self.pos += 1
            return ZInt(cur_token.value)
        elif cur_token.type == Token.Type.FLOAT:
            self.pos += 1
            return ZFloat(cur_token.value)
        elif cur_token.type == Token.Type.STR:
            self.pos += 1
            return ZStr(cur_token.value)

        elif cur_token.type == Token.Type.NONE:
            self.pos += 1
            return ZNone()

        elif cur_token.type == Token.Type.IDN:
            self.pos += 1
            return ZIdn(cur_token.value)

        elif cur_token.type == Token.Type.LZ:
            self.pos += 1
            return ZList(self.get_list())

        elif cur_token.type == Token.Type.LD:
            self.pos += 1
            itms = self.get_set_or_dict()
            if not itms or isinstance(itms[0], ZKeyValuePair):
                return ZDict(itms)
            else:
                return ZSet(itms)

        elif cur_token.type == Token.Type.LP:
            self.pos += 1
            itms, has_comma = self.get_par_if_expr_or_tuple()
            if has_comma:
                return ZTuple(itms)
            else:
                return ZParExpr(itms[0])

    def get_par_if_expr_or_tuple(self):
        self.assert_not_end()
        itms = []
        has_comma = False
        while True:
            cur_token = self.tokens[self.pos]
            if cur_token.type == Token.Type.RP:
                self.pos += 1
                return itms, has_comma
            itms.append(self.get_if_expr())

            cur_token = self.tokens[self.pos]
            if cur_token.type == Token.Type.COMMA:
                has_comma = True
                self.pos += 1

    def get_list(self):
        self.assert_not_end()
        itms = []
        while True:
            cur_token = self.tokens[self.pos]
            if cur_token.type == Token.Type.RZ:
                self.pos += 1
                return itms
            itms.append(self.get_if_expr())
            cur_token = self.tokens[self.pos]
            if cur_token.type == Token.Type.COMMA:
                self.pos += 1

    def get_set_or_dict(self):
        self.assert_not_end()
        itms = []
        while True:
            cur_token = self.tokens[self.pos]
            if cur_token.type == Token.Type.RD:
                self.pos += 1
                return itms
            cur_pos = self.pos
            try:
                expr = self.get_kv_pair()
            except:
                self.pos = cur_pos
                expr = self.get_if_expr()
            itms.append(expr)

            cur_token = self.tokens[self.pos]
            if cur_token.type == Token.Type.COMMA:
                self.pos += 1

    def get_kv_pair(self):
        self.assert_not_end()
        k = self.get_if_expr()
        cur_token = self.tokens[self.pos]
        if cur_token.type == Token.Type.COLON:
            self.pos += 1
        else:
            raise Exception(rf'期望:{Token.Type.COLON}')
        v = self.get_if_expr()
        return ZKeyValuePair(k, v)

    def get_pow(self):
        self.assert_not_end()
        b = self.get_factor()
        cur_token = self.tokens[self.pos]
        if cur_token.type == Token.Type.POW:
            self.pos += 1
            p = self.get_factor()
            return ZPow(b, p)
        else:
            return b

    def get_item(self):
        self.assert_not_end()
        cur_token = self.tokens[self.pos]
        if cur_token.type == Token.Type.SUB:
            self.pos += 1
            ret = ZNeg(self.get_pow())
        else:
            ret = self.get_pow()
        while True:
            cur_token = self.tokens[self.pos]
            if cur_token.type == Token.Type.MUL:
                self.pos += 1
                ret = ZMul(ret, self.get_pow())
            elif cur_token.type == Token.Type.DIV:
                self.pos += 1
                ret = ZDiv(ret, self.get_pow())
            elif cur_token.type == Token.Type.FLOOR_DIV:
                self.pos += 1
                ret = ZFloorDiv(ret, self.get_pow())
            elif cur_token.type == Token.Type.MOD:
                self.pos += 1
                ret = ZMod(ret, self.get_pow())
            else:
                return ret

    def get_expr(self):
        self.assert_not_end()
        ret = self.get_item()
        while True:
            cur_token = self.tokens[self.pos]
            if cur_token.type == Token.Type.ADD:
                self.pos += 1
                ret = ZAdd(ret, self.get_pow())
            elif cur_token.type == Token.Type.SUB:
                self.pos += 1
                ret = ZSub(ret, self.get_pow())
            else:
                return ret

    def get_cmp(self):
        self.assert_not_end()
        ret = self.get_expr()
        while True:
            cur_token = self.tokens[self.pos]
            if cur_token.type == Token.Type.EQ:
                self.pos += 1
                ret = ZEq(ret, self.get_expr())
            elif cur_token.type == Token.Type.NE:
                self.pos += 1
                ret = ZNe(ret, self.get_expr())
            elif cur_token.type == Token.Type.GT:
                self.pos += 1
                ret = ZGt(ret, self.get_expr())
            elif cur_token.type == Token.Type.GE:
                self.pos += 1
                ret = ZGe(ret, self.get_expr())
            elif cur_token.type == Token.Type.LT:
                self.pos += 1
                ret = ZLt(ret, self.get_expr())
            elif cur_token.type == Token.Type.LE:
                self.pos += 1
                ret = ZLe(ret, self.get_expr())
            else:
                return ret

    def get_not(self):
        self.assert_not_end()
        cur_token = self.tokens[self.pos]
        if cur_token.type == Token.Type.NOT:
            self.pos += 1
            return ZNot(self.get_cmp())
        else:
            cur_token = self.tokens[self.pos]
            if cur_token.type == Token.Type.TRUE:
                self.pos += 1
                return ZTrue()
            elif cur_token.type == Token.Type.FALSE:
                self.pos += 1
                return ZFalse()
            else:
                return self.get_cmp()

    def get_and(self):
        self.assert_not_end()
        ret = self.get_not()
        while True:
            cur_token = self.tokens[self.pos]
            if cur_token.type == Token.Type.AND:
                self.pos += 1
                ret = ZAnd(ret, self.get_not())
            else:
                return ret

    def get_or(self):
        self.assert_not_end()
        ret = self.get_and()
        while True:
            cur_token = self.tokens[self.pos]
            if cur_token.type == Token.Type.OR:
                self.pos += 1
                ret = ZOr(ret, self.get_and())
            else:
                return ret

    def get_if_expr(self):
        self.assert_not_end()
        return self.get_or()

    def get_def_arg(self):
        self.assert_not_end()
        cur_token = self.tokens[self.pos]
        if cur_token.type in (Token.Type.MUL,Token.Type.POW):
            self.pos += 1

        cur_token = self.tokens[self.pos]
        if cur_token.type == Token.Type.IDN:
            idn = cur_token.value
            self.pos += 1
        else:
            raise Exception(rf'期望:{Token.Type.IDN},但是是{cur_token}')

        cur_token = self.tokens[self.pos]
        if cur_token.type == Token.Type.COLON:
            self.pos += 1
            type_ = self.get_if_expr()
        else:
            type_ = None

        cur_token = self.tokens[self.pos]
        has_default = False
        if cur_token.type == Token.Type.ASSIGN:
            self.pos += 1
            has_default = True
            default_value = self.get_if_expr()
        else:
            default_value = None

        return idn, type_, has_default, default_value

    def search_func_def(self, func_name):
        self.pos = 0
        try:
            self.assert_not_end()
        except:
            return None
        cur_token = self.tokens[self.pos]
        self.pos += 1

        while True:
            while cur_token.type != Token.Type.DEF:
                try:
                    self.assert_not_end()
                except:
                    return None
                cur_token = self.tokens[self.pos]
                self.pos += 1

            cur_token = self.tokens[self.pos]
            if cur_token.type == Token.Type.IDN and cur_token.value == func_name:
                self.pos += 1
                break

        cur_token = self.tokens[self.pos]
        if cur_token.type != Token.Type.LP:
            return None
        else:
            self.pos += 1
        args = []
        while True:
            cur_token = self.tokens[self.pos]
            if cur_token.type == Token.Type.RP:
                self.pos += 1
                return {
                    'func_name': func_name,
                    'args': args
                }

            args.append(self.get_def_arg())
            cur_token = self.tokens[self.pos]
            if cur_token.type == Token.Type.COMMA:
                self.pos += 1


if __name__ == '__main__':
    with open(r"D:\weiyun\pythonprj\lintcode\lc313.py", 'r', encoding='utf-8') as f:
        code_text = f.read()
    tokens = get_tokens(code_text)
    # print(*tokens, sep='\n')
    agent = SyntaxAgent(tokens)
    a = agent.search_func_def('ffff')

    print(a)
    if a:
        print(*a['args'], sep='\n')
        for x in a['args']:
            if x[2]:
                print(rf'{x[0]}={x[3]}')
            else:
                print(x[0])
