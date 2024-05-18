import re

ZERO = '零〇'
ONE = '壹一'
TWO = '贰二两俩倆'
THREE = '叁三'
FOUR = '肆四'
FIVE = '伍五'
SIX = '陆六'
SEVEN = '柒七'
EIGHT = '捌八'
NINE = '玖九'
TEN = '拾十'
HUNDRED = '佰百'
THOUSAND = '仟千'
TEN_THOUSAND = '万萬'
HUNDRED_MILLION = '亿億'

CHNS_MAP = {
    0: ZERO,
    1: ONE,
    2: TWO,
    3: THREE,
    4: FOUR,
    5: FIVE,
    6: SIX,
    7: SEVEN,
    8: EIGHT,
    9: NINE,
    10: TEN,
    100: HUNDRED,
    1000: THOUSAND,
    10000: TEN_THOUSAND,
    10000_0000: HUNDRED_MILLION
}

CHN_MAP = {k: v[0] for k, v in CHNS_MAP.items()}

NUM_MAP = {}

for num, chns in CHNS_MAP.items():
    for chn in chns:
        NUM_MAP[chn] = num


def _num2chn(num):
    if num < 0:
        return rf'负{_num2chn(-num)}'
    elif num == 0:
        return CHN_MAP[0]
    elif num < 1:
        ret_digits = []
        while num != 0 and len(ret_digits) < 2:
            num *= 10
            cur_d = int(num)
            ret_digits.append(CHN_MAP[cur_d])
            num -= cur_d
        return '点' + "".join(d for d in ret_digits)

    elif num < 10:
        hi = int(num)
        lo = num - hi
        if lo == 0:
            return CHN_MAP[hi]
        else:
            return rf'{CHN_MAP[hi]}{_num2chn(lo)}'
    elif num < 100:
        hi = num // 10
        lo = num % 10
        if lo == 0:
            return rf'{_num2chn(hi)}{CHN_MAP[10]}'
        else:
            return rf'{_num2chn(hi)}{CHN_MAP[10]}{_num2chn(lo)}'

    elif num < 1000:
        hi = num // 100
        lo = num % 100
        if lo == 0:
            return rf'{_num2chn(hi)}{CHN_MAP[100]}'
        elif lo < 10:
            return rf'{_num2chn(hi)}{CHN_MAP[100]}{CHN_MAP[0]}{_num2chn(lo)}'
        else:
            return rf'{_num2chn(hi)}{CHN_MAP[100]}{_num2chn(lo)}'

    elif num < 10000:
        hi = num // 1000
        lo = num % 1000
        if lo == 0:
            return rf'{_num2chn(hi)}{CHN_MAP[1000]}'
        elif lo < 100:
            return rf'{_num2chn(hi)}{CHN_MAP[1000]}{CHN_MAP[0]}{_num2chn(lo)}'
        else:
            return rf'{_num2chn(hi)}{CHN_MAP[1000]}{_num2chn(lo)}'

    elif num < 10000_0000:
        hi = num // 10000
        lo = num % 10000
        if lo == 0:
            return rf'{_num2chn(hi)}{CHN_MAP[10000]}'
        elif lo < 1000:
            return rf'{_num2chn(hi)}{CHN_MAP[10000]}{CHN_MAP[0]}{_num2chn(lo)}'
        else:
            return rf'{_num2chn(hi)}{CHN_MAP[10000]}{_num2chn(lo)}'
    else:
        hi = num // 10000_0000
        lo = num % 10000_0000
        if lo == 0:
            return rf'{_num2chn(hi)}{CHN_MAP[10000_0000]}'
        elif lo < 1000_0000:
            return rf'{_num2chn(hi)}{CHN_MAP[10000_0000]}{CHN_MAP[0]}{_num2chn(lo)}'
        else:
            return rf'{_num2chn(hi)}{CHN_MAP[10000_0000]}{_num2chn(lo)}'


def chn2num(chn: str):
    if not chn:
        return 0
    if chn[0] == '负':
        return -chn2num(chn[1:])
    point_index = chn.find('点')
    if point_index > -1:
        point_num = sum(NUM_MAP[chn[i]] * 10 ** (point_index - i) for i in range(point_index + 1, len(chn)))
        int_num = chn2num(chn[:point_index])
        return point_num + int_num

    reg = re.split(rf'[{HUNDRED_MILLION}]', chn)
    if len(reg) > 2:
        raise ArithmeticError(rf'数字格式错误 ： {chn}')
    elif len(reg) == 2:
        hi = reg[0]
        lo = reg[1]
        if lo in NUM_MAP and NUM_MAP[lo] < 10:
            return (chn2num(reg[0]) if reg[0] else 1) * 1_0000_0000 + chn2num(reg[1]) * 1000_0000
        if lo and lo[0] in ZERO:
            lo = lo[1:]
        return (chn2num(hi) if hi else 1) * 1_0000_0000 + chn2num(lo)

    reg = re.split(rf'[{TEN_THOUSAND}]', chn)
    if len(reg) > 2:
        raise ArithmeticError(rf'数字格式错误 ： {chn}')
    elif len(reg) == 2:
        hi = reg[0]
        lo = reg[1]
        if lo in NUM_MAP and NUM_MAP[lo] < 10:
            return (chn2num(reg[0]) if reg[0] else 1) * 1_0000 + chn2num(reg[1]) * 1000
        if lo and lo[0] in ZERO:
            lo = lo[1:]
        return (chn2num(hi) if hi else 1) * 1_0000 + chn2num(lo)

    reg = re.split(rf'[{THOUSAND}]', chn)
    if len(reg) > 2:
        raise ArithmeticError(rf'数字格式错误 ： {chn}')
    elif len(reg) == 2:
        hi = reg[0]
        lo = reg[1]
        if lo in NUM_MAP and NUM_MAP[lo] < 10:
            return (chn2num(reg[0]) if reg[0] else 1) * 1_000 + chn2num(reg[1]) * 100
        if lo and lo[0] in ZERO:
            lo = lo[1:]
        return (chn2num(hi) if hi else 1) * 1_000 + chn2num(lo)

    reg = re.split(rf'[{HUNDRED}]', chn)
    if len(reg) > 2:
        raise ArithmeticError(rf'数字格式错误 ： {chn}')
    elif len(reg) == 2:
        hi = reg[0]
        lo = reg[1]
        if lo in NUM_MAP and NUM_MAP[lo] < 10:
            return (chn2num(reg[0]) if reg[0] else 1) * 1_00 + chn2num(reg[1]) * 10
        if lo and lo[0] in ZERO:
            lo = lo[1:]
        return (chn2num(hi) if hi else 1) * 1_00 + chn2num(lo)

    reg = re.split(rf'[{TEN}]', chn)
    if len(reg) > 2:
        raise ArithmeticError(rf'数字格式错误 ： {chn}')
    elif len(reg) == 2:
        return (chn2num(reg[0]) if reg[0] else 1) * 1_0 + chn2num(reg[1])

    if chn not in NUM_MAP:
        raise ArithmeticError(rf'数字格式错误 ： {chn}')

    return NUM_MAP[chn]


if __name__ == '__main__':
    print(chn2num('亿'))
