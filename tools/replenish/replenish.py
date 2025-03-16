def get_supplies():
    return {
        '851': 111,
        '852': 111,
    }


def get_demands():
    return {
        'ANA_ADC': 12,
        'SHW_ADC': 31,
    }


def normalize_data(data: dict, total_value: int):
    original_ttl = sum(v for v in data.values())
    if original_ttl == 0:
        return {k: 0 for k, v in data.items()}
    res = {k: int(v / original_ttl * total_value) for k, v in data.items()}
    gap = total_value - sum(v for v in res.values())
    for k, v in sorted(res.items(), key=lambda x: x[1]):
        if gap <= 0:
            break
        if res[k] < data[k]:
            res[k] += 1
            gap -= 1

    return res


def compute_replenishment(supply_map: dict, demand_map: dict):
    total_supply = sum(v for v in supply_map.values())
    total_demand = sum(v for v in demand_map.values())

    if total_supply > total_demand:
        supply_map = normalize_data(supply_map, total_demand)
    elif total_supply < total_demand:
        demand_map = normalize_data(demand_map, total_supply)

    print('供应数据：')
    print(*supply_map.items(), sep='\n')
    print('需求数据：')
    print(*demand_map.items(), sep='\n')
    print()

    res = []
    for s_wh, s_q in supply_map.items():
        cur_repl = normalize_data(demand_map, s_q)
        res.extend([{
            'from_wh': s_wh,
            'to_wh': k,
            'qty': v,
        } for k, v in cur_repl.items() if v > 0])
        demand_map = {k: v - cur_repl[k] for k, v in demand_map.items()}

    return res


if __name__ == '__main__':
    res = compute_replenishment(get_supplies(), get_demands())
    print(*res, sep='\n')
