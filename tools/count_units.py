def get_measure(funits: dict):
    class Measure:
        def __init__(self, num: float, unit: str = min(funits, key=lambda x: funits[x])):
            self.num = num
            self.unit = unit

        @property
        def value(self):
            return self.num*funits[self.unit]

        def __neg__(self):
            return Measure(-self.num, self.unit)

        def __abs__(self):
            return Measure(abs(self.num),self.unit)

        def __add__(self, other: 'Measure'):
            return Measure((self.value + other.value) / funits[self.unit], self.unit)

        def __sub__(self, other: 'Measure'):
            return self + -other

        def show(self, unit: str):
            return f'{self.value / funits[unit]}{unit}'

        def __str__(self):
            return f'{self.num}{self.unit}'

        @classmethod
        def sort(cls, *lenths):
            return sorted(lenths, key=lambda x: x.value)

    return Measure


Length = get_measure({
    '千米': 1000 * 1000,
    '米': 1000,
    '分米': 100,
    '厘米': 10,
    '毫米': 1,
})

Weight = get_measure({
    '吨': 1000 ** 3,
    '千克': 1000 ** 2,
    '克': 1000,
    '毫克': 1,
})

TimeLen = get_measure({
    '小时': 3600 * 1000 ** 3,
    '分': 60 * 1000 ** 3,
    '秒': 1000 ** 3,
    '毫秒': 1000 ** 2,
    '微秒': 1000,
    '纳秒': 1,
})

if __name__ == '__main__':
    a = [
        Weight(950, '克'),
        Weight(905, '克'),
        Weight(1, '千克'),
        Weight(900, '千克'),
        Weight(9000, '克'),
    ]
    a = sorted([Weight(1.003, '吨'), Weight(9998, '千克'), Weight(999, '克')], key=lambda x: abs(x.num - Weight(1, '吨').num))

    for w in a:
        print(abs(Weight(1, '吨')-w).show('吨'))

    print(Length(1, '千米').show('毫米'))
