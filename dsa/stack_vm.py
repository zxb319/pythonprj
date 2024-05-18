import re
from re import Pattern
from typing import Callable, List, Tuple


class StackVM:
    REGs: List[Tuple[Pattern, Callable]] = [
        (re.compile(r'\s*push\s+([\d.+\-]+)\s*', re.IGNORECASE), lambda m, s: s._push(float(m.group(1)))),
        (re.compile(r'\s*pop\s*', re.IGNORECASE), lambda m, s: s._pop()),
        (re.compile(r'\s*add\s*', re.IGNORECASE), lambda m, s: s._alu_op('+')),
        (re.compile(r'\s*sub\s*', re.IGNORECASE), lambda m, s: s._alu_op('-')),
        (re.compile(r'\s*mul\s*', re.IGNORECASE), lambda m, s: s._alu_op('*')),
        (re.compile(r'\s*div\s*', re.IGNORECASE), lambda m, s: s._alu_op('/')),

    ]

    ALU_OP_FUNCs = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b,
    }

    def __init__(self):
        self._stack = []

    def _push(self, val):
        self._stack.append(val)

    def _pop(self):
        if not self._stack:
            raise RuntimeError(rf'STACK Empty!')
        return self._stack.pop()

    def _alu_op(self, op_str: str):
        if op_str not in StackVM.ALU_OP_FUNCs:
            raise RuntimeError(rf'do not support ALU OP:{op_str}!')
        b = self._pop()
        a = self._pop()
        r = StackVM.ALU_OP_FUNCs[op_str](a, b)
        self._push(r)

    def exec(self, cmd: str):
        found = False
        for r, f in StackVM.REGs:
            m = r.match(cmd)
            if m:
                found = True
                ret = f(m, self)
                print(self._stack, ret)
        if not found:
            raise RuntimeError(rf'not supported cmd:{cmd}!')


if __name__ == '__main__':
    stack_vm = StackVM()
    while True:
        print(">>>", end='')
        cmd = input()
        cmd = cmd.strip()
        if not cmd:
            continue
        try:
            stack_vm.exec(cmd)
        except Exception as e:
            print(rf'error:{e}')
