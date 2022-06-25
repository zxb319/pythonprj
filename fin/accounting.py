def make_balance_sheet(initial_balance_sheet: dict, accounting_events: list):
    for event in accounting_events:
        """(科目，明细，科目，明细，金额)"""
        if event[1] not in initial_balance_sheet[event[0]]:
            initial_balance_sheet[event[0]][event[1]] = 0
        if event[3] not in initial_balance_sheet[event[2]]:
            initial_balance_sheet[event[2]][event[3]] = 0

        if event[0] in ('资产', '费用'):
            initial_balance_sheet[event[0]][event[1]] += event[4]
        else:
            initial_balance_sheet[event[0]][event[1]] -= event[4]

        if event[2] in ('资产', '费用'):
            initial_balance_sheet[event[2]][event[3]] -= event[4]
        else:
            initial_balance_sheet[event[2]][event[3]] += event[4]

    return initial_balance_sheet


def print_banlance_sheet(banlance_sheet: dict):
    print('资产:')
    for itm in banlance_sheet['资产'].items():
        print(itm[0], itm[1])

    print('负债:')
    for itm in banlance_sheet['负债'].items():
        print(itm[0], itm[1])

    print('所有者权益:')
    for itm in banlance_sheet['所有者权益'].items():
        print(itm[0], itm[1])

    print('收入:')
    for itm in banlance_sheet['收入'].items():
        print(itm[0], itm[1])

    print('费用:')
    for itm in banlance_sheet['费用'].items():
        print(itm[0], itm[1])

    print('资产费用总计:', sum(v for v in banlance_sheet['资产'].values())
          +sum(v for v in banlance_sheet['费用'].values())
          )
    print('负债加所有者权益:',
          sum(v for v in banlance_sheet['负债'].values())
          + sum(v for v in banlance_sheet['所有者权益'].values())
          + sum(v for v in banlance_sheet['收入'].values())
          )


if __name__ == '__main__':
    initial_banlance_sheet = {
        '资产': {
            '库存现金': 2000,
            '银行存款': 50000,
            '应收票据': 60000,
            '应收账款': 30000,
            '原材料': 100000,
            '固定资产': 250000,

        },
        '负债': {
            '短期借款': 36000,
            '应付票据': 34000,
            '应付账款': 52000,

        },
        '所有者权益': {
            '实收资本': 300000,
            '盈余公积': 48000,
            '未分配利润': 22000,

        },
        '收入':{},
        '费用':{},
    }

    accounting_events=[
        ('资产', '原材料','负债','应付账款',5000),
        ('负债', '短期借款', '资产', '银行存款',20000),
        ('资产', '银行存款', '资产', '应收账款',10000),
        ('负债', '应付账款', '负债', '应付票据',5000),
        ('所有者权益', '盈余公积', '所有者权益', '实收资本',30000),
        ('资产', '固定资产', '所有者权益','实收资本',50000),
        ('所有者权益', '实收资本', '资产', '银行存款',10000),
        ('所有者权益', '未分配利润', '负债', '应付股利',5000),
        ('负债', '应付账款', '所有者权益', '实收资本',10000),
        ('资产','银行存款','收入','主营业务收入',40000),
        ('费用','管理费用','资产','原材料',5000),


    ]

    # print_banlance_sheet(initial_banlance_sheet)
    banlance_sheet=make_balance_sheet(initial_banlance_sheet,accounting_events)

    print_banlance_sheet(banlance_sheet)
