from fin.time_value import irr

class Bond:
    def __init__(self, cash_values: list[float], ):
        self.cash_values = cash_values

    def yield_to_maturity(self):
        """
        债券的到期收益率
        """
        return irr(self.cash_values)


def compute_spot_rates(bonds: list[Bond]):
    """计算债券所有期限的即期利率
    0~1 0~2 ... 0~T的T个年化利率
    """
    ret = {}
    bond_map = {len(b.cash_values) - 1: b for b in bonds}

    def inner(period_count: int):
        if period_count == 0:
            return
        else:
            inner(period_count - 1)
            cur_bond = bond_map[period_count]
            cur_pv = cur_bond.cash_values[0]
            for i, c in enumerate(cur_bond.cash_values[1:-1]):
                r = ret[i + 1]
                cur_pv += c / (1 + r) ** (i + 1)

            ret[period_count] = ((-cur_bond.cash_values[-1] / cur_pv)
                                 ** (1 / (len(cur_bond.cash_values) - 1))
                                 - 1)

    inner(max(bond_map))

    return ret


def compute_bond_pv(bond_future_cash_values: list, spot_rates: dict):
    """
    给定债券的未来现金流和所有期限的即期利率
    求 债券的现值
    """
    if len(bond_future_cash_values) > len(spot_rates):
        raise Exception(rf'spot_rates不足：{spot_rates}')
    ret = 0
    for i, (c, r) in enumerate(zip(bond_future_cash_values, sorted(spot_rates.items()))):
        ret += c / (1 + r[1]) ** (i + 1)

    return ret


if __name__ == '__main__':

    import math
    bs = [
        Bond([-95, 100]),
        Bond([-97, 5, 5 + 100]),
    ]

    r = compute_spot_rates(bs)

    pv=compute_bond_pv([6,6+100],r)

    print(pv)
