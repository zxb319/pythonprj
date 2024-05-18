import functools
import math
import re


class Token:
    class Type:
        NUM = 'NUM'
        VAR = 'VAR'
        ADD = 'ADD'
        SUB = 'SUB'
        MUL = 'MUL'
        DIV = 'DIV'
        POW = 'POW'
        LP = 'LP'
        RP = 'RP'

    def __init__(self, typ, val):
        self.typ = typ
        self.val = val

    def __str__(self):
        return rf'<{self.typ}:{self.val}>'


def get_tokens(s: str):
    regs = [

        r'^\+',
        r'^\-',
        r'^\^\^',
        r'^\*',
        r'^/',
        r'^\(',
        r'^\)',
        r'^\s+',
        r'^[_a-z]+[_a-z0-9]*',
        r'^,',
    ]

    regs=[
        (Token.Type.NUM,r'^\d+\.?(\d+)?(e[+\-]?\d+)?'),
        (Token.Type.NUM,r'^\.\d+(e[+\-]?\d+)?',),
        (Token.Type.ADD),
        (Token.Type.ADD),
        (Token.Type.ADD),
        (Token.Type.ADD),
        (Token.Type.ADD),
        (Token.Type.ADD),
        (Token.Type.ADD),
        (Token.Type.ADD),
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
        r'^\d+\.?(\d+)?(e[+\-]?\d+)?$',
        r'^\.\d+(e[+\-]?\d+)?$',
    ]
    for r in regs:
        reg = re.search(r, t, re.IGNORECASE)
        if reg:
            return True

    return False


def is_func_name(t):
    reg = re.search(r'^[_a-z]+[_a-z0-9]*$', t, re.IGNORECASE)
    return reg is not None


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


_funcs = {
    'log': lambda a, b: math.log(b, a),
    'sin': lambda x: math.sin(x),
    'cos': lambda x: math.cos(x),
    'tan': lambda x: math.tan(x),
    'cot': lambda x: 1 / math.tan(x),
    'pi': lambda: math.pi,
    'e': lambda: math.e
}


class FuncCall:
    def __init__(self, func_name, *args):
        f = _funcs.get(func_name)
        if not f:
            raise ArithmeticError(rf'不支持：{func_name}！')

        args = [a.value for a in args]
        try:
            r = f(*args)
        except Exception as e:
            raise ArithmeticError(rf'报错：{func_name}({",".join(str(ar) for ar in args)}) : {e}')

        self.value = r


class Pol:
    def __init__(self, left, right):
        self.value = left.value ** right.value


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
def is_pol_factor(tks):
    locs = list(find_loc(tks, ['^^']))
    for pl in locs:
        a = is_factor(tks[pl + 1:])
        b = is_factor(tks[:pl])
        if a and b:
            return True

    return False


@cache
def is_paras(tks):
    if not tks:
        return True
    comma_loc = find_loc(tks, ',')

    a = is_expr(tks)
    if a:
        return True

    for cl in comma_loc:
        a = is_expr(tks[:cl])
        b = is_paras(tks[cl + 1:])
        if a and b:
            return True

    return False


@cache
def is_func_factor(tks):
    if len(tks) < 3:
        return False

    if not is_func_name(tks[0]):
        return False

    if tks[1] != '(':
        return False

    if tks[-1] != ')':
        return False

    return is_paras(tks[2:-1])


@cache
def is_factor(tks):
    return is_num_factor(tks) or is_expr_factor(tks) or is_pol_factor(tks) or is_func_factor(tks)


@cache
def is_neg_term(tks):
    return len(tks) >= 2 and tks[0] in '+-' and is_term(tks[1:])


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
    return is_factor(tks) or is_neg_term(tks) or is_mul_term(tks)


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
    if is_pol_factor(tks):
        locs = list(find_loc(tks, ['^^']))
        for pl in locs:
            a = is_factor(tks[pl + 1:])
            b = is_factor(tks[:pl])
            if a and b:
                left = get_factor(tks[:pl])
                right = get_factor(tks[pl + 1:])
                return Pol(left, right)

    if is_func_factor(tks):
        def get_paras(ttkkss):
            if not ttkkss:
                return []

            comma_loc = find_loc(ttkkss, ',')
            a = is_expr(ttkkss)
            if a:
                return [get_expr(ttkkss)]

            for cl in comma_loc:
                a = is_expr(ttkkss[:cl])
                b = is_paras(ttkkss[cl + 1:])
                if a and b:
                    return [get_expr(ttkkss[:cl])] + get_paras(ttkkss[cl + 1:])

            raise Exception(rf'语法错误:{ttkkss}')

        paras = get_paras(tks[2:-1])
        return FuncCall(tks[0], *paras)

    raise Exception(rf'语法错误:{tks}')


def get_term(tks):
    if is_factor(tks):
        return get_factor(tks)

    if is_neg_term(tks):
        if tks[0] == '+':
            return get_term(tks[1:])
        else:
            return Neg(get_term(tks[1:]))

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

    raise Exception(rf'语法错了！{tks}')


if __name__ == '__main__':
    expr_s = r'''
        log(2,-log(e(),e()^^(-8)))
    '''
    tokens = list(get_tokens(expr_s.strip()))
    print((tokens))
    # print(tokens)
    # print(*globals().items(),sep='\n')
    a = get_expr(tks=tokens)
    print(a.value)
