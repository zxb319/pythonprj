
from script_gen import *


if __name__ == '__main__':
    data = {
        'case_id': 'case_id1',
        'case_name': '用例名称1',
        'processes': [
            {
                'type': 'restore',
                'steps': [
                    {
                        'type': 'parallel',
                        'code_head_kwargs': {'time_slot':2}, #'times':2
                        'desc': '强制执行1',
                        'step_body_segments': [
                            {
                                'type': 'combine',
                                'kwargs': {
                                    'name': '组合1',
                                    'commands': [
                                        {
                                            'type': 'logic',
                                            'kwargs': {
                                                'func_name': 'Logic_Func_11',
                                                'args': [
                                                    {
                                                        'name': 'a1',
                                                        'value': {
                                                            'type': 'expression',
                                                            'value': '[1,e,3]'
                                                        },
                                                    },
                                                    {
                                                        'name': 'a2',
                                                        'value': {
                                                            'type': 'expression',
                                                            'value': '1+3'
                                                        },
                                                    },
                                                ],
                                            },
                                        }
                                    ],
                                },
                            },
                            {
                                'type': 'command',
                                'kwargs': {
                                    'type': 'action',
                                    'kwargs': {
                                        'entity': 'XCP_1_0',
                                        'signal': 'sleee',
                                        'operator': '==',
                                        'value': '2',
                                        'arg': 'None',
                                        'valid_time': 3,
                                    },
                                }
                            },
                            {
                                'type': 'command',
                                'kwargs': {
                                    'type': 'assign',
                                    'kwargs': {
                                        'left': 'var1',
                                        'right': {
                                            'type': 'constant',
                                            'value': 'we'
                                        },
                                    },
                                }
                            },
                        ],
                    },
                ],
            },
        ]
    }
    case = CaseScript(data)

    print(case)