import math
from typing import List


class Bond:
    def __init__(self, cash_values: list, ):
        self.cash_values = cash_values


def compute_spot_rates(bonds: List[Bond]):
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

            ret[period_count] = (-cur_bond.cash_values[-1] / cur_pv) ** (1 / (len(cur_bond.cash_values) - 1)) - 1

    inner(max(bond_map))

    return ret


def compute_bond_pv(bond_future_cash_values: List, spot_rates: dict):
    if len(bond_future_cash_values) > len(spot_rates):
        raise Exception(rf'spot_rates不足：{spot_rates}')
    ret = 0
    for i, (c, r) in enumerate(zip(bond_future_cash_values, sorted(spot_rates.items()))):
        ret += c / (1 + r[1]) ** (i + 1)

    return ret


if __name__ == '__main__':
    bonds = [
        Bond([-98, 100]),
        Bond([-104, 6, 6 + 100]),
        Bond([-111, 8, 8, 8 + 100]),
        Bond([-102, 5, 5, 5, 5 + 100]),
    ]

    r = compute_spot_rates(bonds)
    print({k: math.log(1 + v, math.e) for k, v in r.items()})
