class NandGate:
    def __call__(self, a: bool, b: bool):
        return not (a and b)


class NotGate:
    def __init__(self):
        self._nand_gate = NandGate()

    def __call__(self, a: bool):
        return self._nand_gate(a, a)


class AndGate:
    def __init__(self):
        self._nand_gate = NandGate()
        self._not_gate = NotGate()

    def __call__(self, a: bool, b: bool):
        r1 = self._nand_gate(a, b)
        return self._not_gate(r1)


class OrGate:
    def __init__(self):
        self._not_gate1 = NotGate()
        self._not_gate2 = NotGate()
        self._nand_gate = NandGate()

    def __call__(self, a: bool, b: bool):
        r1 = self._not_gate1(a)
        r2 = self._not_gate2(b)
        return self._nand_gate(r1, r2)


if __name__ == '__main__':
    or_gate = OrGate()

    print(or_gate(False, False))
    print(or_gate(False, True))
    print(or_gate(True, False))
    print(or_gate(True, True))
