import re
from collections import deque

import app_tools


def get_kwargs(kwargs: dict, arg_name, required=True, types_={int, float, str}):
    if not isinstance(kwargs,dict):
        raise app_tools.ArgsError(rf'需要 dict!')
    v = kwargs.get(arg_name)
    if required and v is None:
        raise app_tools.ArgsError(rf'{arg_name} is required!')
    if v is None:
        return v

    if type(v) not in types_:
        raise app_tools.ArgsError(rf'{arg_name}的类型不合法，需要{types_}, 给的是{type(v)}')

    return v


def add_indents(code_segment, indent_count):
    lines = code_segment.split('\n')
    lines = [rf"{' ' * 4 * indent_count}{l}" for l in lines]
    return '\n'.join(lines)


def remove_indent(code_segment, indent_count):
    lines = code_segment.split('\n')
    new_lines = []
    for l in lines:
        if l[:indent_count * 4] != ' ' * 4 * indent_count:
            raise app_tools.ArgsError(rf'{code_segment}的缩进数不够反缩进的数量！')
        new_lines.append(l[:4 * indent_count])
    return '\n'.join(new_lines)


def strip_white_lines(code_segment):
    lines = deque(code_segment.split('\n'))

    while not lines[0].strip():
        lines.popleft()

    while not lines[-1].strip():
        lines.pop()

    return '\n'.join(lines)


class CaseScript:
    def __init__(self, kwargs):
        self.case_id = get_kwargs(kwargs, 'case_id')
        self.case_name = get_kwargs(kwargs, 'case_name')
        processes = get_kwargs(kwargs, 'processes', types_={list})
        self.processes = [Process(p) for p in processes]

    def append(self, process):
        self.processes.append(process)

    def __str__(self):
        haven_process_map = {}
        for p in self.processes:
            if p.type in haven_process_map:
                raise app_tools.ArgsError(rf'过程{p.type}重复！')
            haven_process_map[p.type] = p

        segments = [haven_process_map[t] if t in haven_process_map else Process({'type': t, 'steps': []}) for t in Process.Type.TYPES]
        segments = '\n\n'.join(str(p) for p in segments)

        res = rf'''
from cmbird import *
from logic import *

class {self.case_id}(cmbird):
@information(
    case_id='{self.case_id}',
    case_name='{self.case_name}'
)
    def __init__(self):
        Logic_Case_Init(__file__)
        pass
        
{add_indents(segments, 1)}
        '''

        return strip_white_lines(res)


class Process:
    class Type:
        PREPARE = 'prepare'
        PROCESS = 'process'
        POSTLUDE = 'postlude'
        RESTORE = 'restore'
        FAILURE = 'failure'

        TYPES = [PREPARE, PROCESS, POSTLUDE, FAILURE, RESTORE]

        CODE_HEAD_MAP = {
            PREPARE: rf"def prepare(self):",
            PROCESS: rf"def process(self):",
            POSTLUDE: rf"def postlude(self):",
            RESTORE: rf"def restore(self):",
            FAILURE: f'@failure(True)\ndef failure(self):',
        }

    def __init__(self, kwargs):
        self.type = get_kwargs(kwargs, 'type')
        if self.type not in Process.Type.CODE_HEAD_MAP:
            raise app_tools.ArgsError(rf'不支持 process_type={self.type}，可选{Process.Type.TYPES}')

        self.code_head = Process.Type.CODE_HEAD_MAP[self.type]

        steps = get_kwargs(kwargs, 'steps', types_={list})
        self.steps = [Step(s) for s in steps]

    def append(self, step):
        self.steps.append(step)

    def __str__(self):
        segments = [str(s) for s in self.steps]
        segments.append('pass')
        segments = '\n'.join(segments)

        res = rf'''
{self.code_head}
{add_indents(segments, 1)}
        '''

        return strip_white_lines(res)


class Step:
    class Type:
        NORMAL = 'normal'
        FORCE_RUN = 'force_run'
        LOOP_RUN = 'loop_run'
        FORCE_LOOP = 'force_loop'
        ATTEMPT = 'attempt'
        PARALLEL = 'parallel'

        @staticmethod
        def _loop_run_head_func(kwargs):
            times = get_kwargs(kwargs, 'times')
            return rf"with LoopRun(times={times}, loc=globals(), scope=logic) as a:"

        @staticmethod
        def _force_loop_head_func(kwargs):
            times = get_kwargs(kwargs, 'times')
            return rf"with ForceLoop(times={times}, loc=globals(), scope=logic) as a:"

        @staticmethod
        def _attempt_head_func(kwargs):
            times = get_kwargs(kwargs, 'times', False)
            time_slot = get_kwargs(kwargs, 'time_slot', False)

            if times is not None:
                return rf"with Attempt(times={times}, loc=globals(), scope=logic) as a:"
            elif time_slot is not None:
                return rf"with Attempt(time_slot={time_slot}, loc=globals(), scope=logic) as a:"
            else:
                raise app_tools.ArgsError(rf'Attempt times 和 time_slot 二者必填一个！')

        CODE_HEAD_MAP = {
            FORCE_RUN: lambda kwargs: rf"with ForceRun(loc=globals(), scope=logic) as a:",
            PARALLEL: lambda kwargs: rf"with Parallel(loc=globals(), scope=logic) as a:",
            LOOP_RUN: lambda kwargs: Step.Type._loop_run_head_func(kwargs),
            FORCE_LOOP: lambda kwargs: Step.Type._force_loop_head_func(kwargs),
            ATTEMPT: lambda kwargs: Step.Type._attempt_head_func(kwargs),
            NORMAL:lambda kwargs:None,

        }

    def __init__(self, kwargs):
        type_ = get_kwargs(kwargs, 'type')
        self.type = type_
        if type_ not in Step.Type.CODE_HEAD_MAP:
            raise app_tools.ArgsError(rf'Step 不支持{type_}, 只支持：{Step.Type.CODE_HEAD_MAP.keys()}')
        code_head_kwargs = get_kwargs(kwargs, 'code_head_kwargs', types_={dict})
        desc = get_kwargs(kwargs, 'desc')

        self.desc = desc
        if type_ not in Step.Type.CODE_HEAD_MAP:
            raise app_tools.ArgsError(rf'步骤类型不支持{type_}！')
        self.code_head = Step.Type.CODE_HEAD_MAP[type_](code_head_kwargs)
        step_body_segments = get_kwargs(kwargs, 'step_body_segments', types_={list})
        self.step_body_segments = [StepBodySegment(x) for x in step_body_segments]

    def append(self, step_body_segment):
        self.step_body_segments.append(step_body_segment)

    def __str__(self):
        segs = [str(s) for s in self.step_body_segments]
        segs.append('pass')
        segs = '\n'.join(segs)
        segs = [s if s.startswith('#') or not s.strip() or s == 'pass' else rf'a.{s}' for s in segs.split('\n')]
        segs = '\n'.join(segs)
        head=f'\n{self.code_head}' if self.code_head else ''
        res = rf'''
# {self.desc}{head}
{add_indents(segs, 0 if self.type == Step.Type.NORMAL else 1)}
        '''
        return strip_white_lines(res)


class Combine:
    def __init__(self, kwargs):
        self.name = get_kwargs(kwargs, 'name')
        commands = get_kwargs(kwargs, 'commands', types_={list})
        self.commands = [Command(x) for x in commands]

    def append(self, command):
        self.commands.append(command)

    def __str__(self):
        segments = [str(c) for c in self.commands]
        segments = '\n'.join(segments)
        res = rf'''
# {'-' * 10} {self.name} start {'-' * 10}
{segments}
# {'-' * 10} {self.name} end {'-' * 10}
        '''

        return strip_white_lines(res)


class Value:
    class Type:
        CONSTANT = 'constant'
        VARIABLE = 'variable'
        EXPRESSION = 'expression'
        LOGIC_RETURN = 'logic_return'

        @staticmethod
        def _format_constant(v):
            try:
                eval(v)
            except:
                if not re.search(r'''^['"\(\[\{].+['"\)\]\}]$''', v, re.IGNORECASE):
                    return rf"'{v}'"
            return v

        FORMAT_MAP = {
            CONSTANT: lambda v: Value.Type._format_constant(v),
            VARIABLE: lambda v: v,
            EXPRESSION: lambda v: v,
            LOGIC_RETURN: lambda v: v,
        }

    def __init__(self, kwargs):
        type_ = get_kwargs(kwargs, 'type')
        if type_ not in Value.Type.FORMAT_MAP:
            raise app_tools.ArgsError(rf'Value不支持 {type_}, 只支持{Value.Type.FORMAT_MAP.keys()}!')
        value = get_kwargs(kwargs, 'value')

        self.value = Value.Type.FORMAT_MAP[type_](value)

    def __str__(self):
        return str(self.value)


class ActionCommand:
    def __init__(self, kwargs):
        self.entity = get_kwargs(kwargs, 'entity')
        self.signal = get_kwargs(kwargs, 'signal')
        self.operator = get_kwargs(kwargs, 'operator')
        self.value = get_kwargs(kwargs, 'value')
        self.arg = get_kwargs(kwargs, 'arg')
        self.valid_time = get_kwargs(kwargs, 'valid_time', required=False)

        self.value = re.sub(rf'\$arg', self.arg, self.value, flags=re.IGNORECASE)

        self.value = Value({'type': Value.Type.CONSTANT, 'value': self.value})

        self.code = rf"Logic_Func('{self.entity}','{self.signal}','{self.operator}',{self.value}{rf', {self.valid_time}' if self.valid_time is not None else ''})"

    def __str__(self):
        return self.code


class LogicCommand:
    def __init__(self, kwargs):
        self.func_name = get_kwargs(kwargs, 'func_name')
        self.args = get_kwargs(kwargs, 'args', types_={list})

    def __str__(self):
        args = []
        for a in self.args:
            name = get_kwargs(a, 'name')
            value = get_kwargs(a, 'value', types_={dict})
            value = Value(value)
            args.append({'name': name, 'value': value})
        args = [rf'{a["name"]}={a["value"]}' for a in args]
        args = ', '.join(str(a) for a in args)
        res = rf'''
{self.func_name}({args})
        '''
        return strip_white_lines(res)


class AssignCommand:
    def __init__(self, kwargs):
        self.left = get_kwargs(kwargs, 'left')
        self.right = get_kwargs(kwargs, 'right', types_={dict})

    def __str__(self):
        return rf'{self.left} = {Value(self.right)}'


class Command:
    class Type:
        ACTION = 'action'
        LOGIC = 'logic'
        ASSIGN = 'assign'

        CLASS_MAP = {
            ACTION: ActionCommand,
            LOGIC: LogicCommand,
            ASSIGN: AssignCommand,
        }

    def __init__(self, kwargs):
        type_ = get_kwargs(kwargs, 'type')
        if type_ not in Command.Type.CLASS_MAP:
            raise app_tools.ArgsError(rf'不支持{type_}, 只支持{Command.Type.CLASS_MAP.keys()}')

        kwargs = get_kwargs(kwargs, 'kwargs', types_={dict})

        self.command = Command.Type.CLASS_MAP[type_](kwargs)

    def __str__(self):
        return str(self.command)


class StepBodySegment:
    class Type:
        COMBINE = 'combine'
        COMMAND = 'command'

        CLASS_MAP = {
            COMBINE: Combine,
            COMMAND: Command,
        }

    def __init__(self, kwargs):
        type_ = get_kwargs(kwargs, 'type')
        if type_ not in StepBodySegment.Type.CLASS_MAP:
            raise app_tools.ArgsError(rf'StepBody不支持{type_}, 只支持{StepBodySegment.Type.CLASS_MAP.keys()}')
        kwargs = get_kwargs(kwargs, 'kwargs', types_={dict})
        self.body_segment = StepBodySegment.Type.CLASS_MAP[type_](kwargs)

    def __str__(self):
        return str(self.body_segment)


def create_case_script(data):
    case_script = CaseScript(data)
    return case_script



