import re
import time
from typing import List


class Token:
    STR = 'str'
    INT = 'int'
    FLOAT = 'float'
    NULL = 'null'
    BOOL = 'bool'
    COMMA = 'comma'
    COLON = 'colon'
    LZ = 'lz'
    RZ = 'rz'
    LD = 'ld'
    RD = 'rd'
    WHITE = 'white'

    REG_MAP = {
        STR: r'\"[^\"]*\"',
        FLOAT: r'[\+\-]?(\d+\.\d*|\.\d+)(e[\+\-]?\d+)?',
        INT: r'[\+\-]?\d+',
        NULL: r'null',
        BOOL: r'(true|false)',
        COMMA: r'\,',
        COLON: r'\:',
        LZ: r'\[',
        RZ: r'\]',
        LD: r'\{',
        RD: r'\}',
        WHITE: r'\s+'
    }

    REG_MAP = {k: re.compile(v, re.IGNORECASE) for k, v in REG_MAP.items()}

    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return rf'({self.type},{self.value})'


def get_tokens(s):
    ret = []
    pos = 0
    while pos < len(s):
        found = False
        for t, r in Token.REG_MAP.items():
            reg = r.match(s, pos)
            if reg:
                found = True
                if t != Token.WHITE:
                    ret.append(Token(t, reg.group(0)))
                pos += len(reg.group(0))
                break

        if not found:
            raise Exception(rf'无法识别的符号：{s}')
    return ret


class Int:
    def __init__(self, value):
        self._value = int(value)

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self._value)


class Float:
    def __init__(self, value):
        self._value = float(value)

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self._value)


class Str:
    def __init__(self, value):
        self._value = value[1:-1]

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self._value)


class Null:
    def __init__(self):
        self._value = None

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self.value)


class Bool:
    def __init__(self, value):
        self._value = value.lower() == 'true'

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self._value)


class JList:
    def __init__(self, values: list):
        self._value = list(x.value for x in values)

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self.value)


class JDict:
    def __init__(self, kv_pairs: list):
        self._value = {x[0].value: x[1].value for x in kv_pairs}

    @property
    def value(self):
        return self._value

    def __str__(self):
        return str(self.value)


def get_jlist(tokens: List[Token], lo: int):
    items = []
    while True:
        if lo >= len(tokens):
            raise Exception('语法错误！')

        if tokens[lo].type in (Token.RZ,):
            return JList(items), lo + 1

        itm, lo = get_json_part(tokens, lo)
        items.append(itm)
        if lo >= len(tokens):
            raise Exception('语法错误！')
        if tokens[lo].type == Token.COMMA:
            lo += 1


def get_str(tokens: List[Token], lo: int):
    if lo >= len(tokens) or tokens[lo].type != Token.STR:
        raise Exception('语法错误！')

    return Str(tokens[lo].value), lo + 1


def get_colon(tokens: List[Token], lo: int):
    if lo >= len(tokens) or tokens[lo].type != Token.COLON:
        raise Exception('语法错误！')

    return lo + 1


def get_jdict(tokens: List[Token], lo: int):
    items = []
    while True:
        if lo >= len(tokens):
            raise Exception('语法错误！')

        if tokens[lo].type == Token.RD:
            return JDict(items), lo + 1

        k, lo = get_str(tokens, lo)
        lo = get_colon(tokens, lo)
        v, lo = get_json_part(tokens, lo)
        items.append((k, v))
        if lo >= len(tokens):
            raise Exception('语法错误！')
        if tokens[lo].type == Token.COMMA:
            lo += 1


def get_json_part(tokens: List[Token], lo: int):
    if tokens[lo].type == Token.NULL:
        return Null(), lo + 1

    if tokens[lo].type == Token.INT:
        return Int(tokens[lo].value), lo + 1

    if tokens[lo].type == Token.FLOAT:
        return Float(tokens[lo].value), lo + 1

    if tokens[lo].type == Token.STR:
        return Str(tokens[lo].value), lo + 1

    if tokens[lo].type == Token.BOOL:
        return Bool(tokens[lo].value), lo + 1

    if tokens[lo].type == Token.LZ:
        return get_jlist(tokens, lo + 1)

    if tokens[lo].type == Token.LD:
        return get_jdict(tokens, lo + 1)

    raise Exception('语法错误！')


def get_json(tokens: List[Token]):
    r, i = get_json_part(tokens, 0)
    if i < len(tokens):
        raise Exception('语法错误！')
    return r


if __name__ == '__main__':
    # data = [rf'"{i}":{i}' for i in range(10)]
    # data = '{' + ", ".join(data) + '}'
    s = '''
        {
        "name":"shijihong",
        "age":27,
        "gender":"female",
        "hobbies":["reading","travel"],
        "married":false,
        "beloved":true,
        "future_spouse":null,
        "score":98.7
        }

    '''
    s = rf'[{s * 1000}]'
    # print(s)
    start_time = time.time()
    tokens = get_tokens(s)
    print('parse token: ', time.time() - start_time, 's')
    # print(*tokens, sep=' ')

    start_time = time.time()
    a = get_json(tokens)
    print(time.time() - start_time, 's')
    print(*a.value, sep='\n')
