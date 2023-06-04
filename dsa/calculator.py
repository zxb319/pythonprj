import functools
import re


def get_tokens(s: str):
    regs = [
        r'^\d+(\.\d+)?(e[+\-]?\d+)?',
        r'^\.\d+(e[+\-]?\d+)?',
        r'^\+',
        r'^\-',
        r'^\*\*',
        r'^\*',
        r'^/',
        r'^\(',
        r'^\)',
        r'^\s+',
    ]

    while s:
        found = False
        for r in regs:
            reg = re.search(r, s, re.IGNORECASE)
            if reg:
                found = True
                if reg.group(0).replace(' ', ''):
                    yield reg.group(0)
                s = s[len(reg.group(0)):]
                continue

        if not found:
            raise Exception(rf'{s}附近有无法识别的token!')


def is_number_token(t):
    regs = [
        r'^\d+(\.\d+)?(e[+\-]?\d+)?$',
        r'^\.\d+(e[+\-]?\d+)?$',
    ]
    for r in regs:
        reg = re.search(r, t, re.IGNORECASE)
        if reg:
            return True

    return False


def find_loc(tks, ts):
    ret = []
    for i, tt in enumerate(tks):
        if tt in ts:
            ret.append(i)

    return ret


class Value:
    def __init__(self, t):
        self.value = float(t)


class Neg:
    def __init__(self, v):
        self.value = -v.value


class Pos:
    def __init__(self, v):
        self.value = v.value


class Mul:
    def __init__(self, left, right):
        self.value = left.value * right.value


class Div:
    def __init__(self, left, right):
        self.value = left.value / right.value


class Add:
    def __init__(self, left, right):
        self.value = left.value + right.value


class Sub:
    def __init__(self, left, right):
        self.value = left.value - right.value


def cache(func):
    c = dict()

    @functools.wraps(func)
    def inner(*args, **kwargs):
        k = rf'{str(args)}, {str(kwargs)}'
        if k in c:
            return c[k]
        res = func(*args, **kwargs)
        c[k] = res
        return res

    return inner


@cache
def is_num_factor(tks):
    return len(tks) == 1 and is_number_token(tks[0])


@cache
def is_expr_factor(tks):
    return len(tks) >= 3 and tks[0] == '(' and is_expr(tks[1:-1]) and tks[-1] == ')'


@cache
def is_neg_factor(tks):
    return len(tks) >= 2 and tks[0] in '+-' and is_factor(tks[1:])


@cache
def is_factor(tks):
    return is_num_factor(tks) or is_expr_factor(tks) or is_neg_factor(tks)


@cache
def is_mul_term(tks):
    locs = list(reversed(find_loc(tks, '*/')))
    for pl in locs:
        a = is_factor(tks[pl + 1:])
        b = is_term(tks[:pl])
        if a and b:
            return True

    return False


@cache
def is_term(tks):
    return is_factor(tks) or is_mul_term(tks)


@cache
def is_add_expr(tks):
    plus_locs = list(reversed(find_loc(tks, '+-')))
    for pl in plus_locs:
        a = is_term(tks[pl + 1:])
        b = is_expr(tks[:pl])
        if a and b:
            return True

    return False


@cache
def is_expr(tks):
    return is_term(tks) or is_add_expr(tks)


def get_factor(tks):
    if is_num_factor(tks):
        return Value(tks[0])
    if is_expr_factor(tks):
        return get_expr(tks[1:-1])
    if is_neg_factor(tks):
        if tks[0] == '+':
            return get_factor(tks[1:])
        else:
            return Neg(get_factor(tks[1:]))
    raise Exception('语法错误')


def get_term(tks):
    if is_factor(tks):
        return get_factor(tks)

    locs = list(reversed(find_loc(tks, '*/')))
    for pl in locs:
        a = is_factor(tks[pl + 1:])
        b = is_term(tks[:pl])
        if a and b:
            left = get_term(tks[:pl])
            right = get_factor(tks[pl + 1:])
            if tks[pl] == '*':
                return Mul(left, right)
            else:
                return Div(left, right)
    raise Exception(rf'语法错误！{tks}')


def get_expr(tks):
    if is_term(tks):
        return get_term(tks)

    plus_locs = list(reversed(find_loc(tks, '+-')))
    for pl in plus_locs:
        a = is_term(tks[pl + 1:])
        b = is_expr(tks[:pl])
        if a and b:
            left = get_expr(tks[:pl])
            right = get_term(tks[pl + 1:])
            if tks[pl] == '+':
                return Add(left, right)
            else:
                return Sub(left, right)

    raise Exception('语法错了！')


if __name__ == '__main__':
    tokens = list(get_tokens(''))
    # print(tokens)
    # print(*globals().items(),sep='\n')
    a = get_expr(tks=tokens)
    print(a.value)
