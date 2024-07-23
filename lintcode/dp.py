def package(apples: list, bag_vol: int):
    res = 0
    for a in apples:
        if not a.get('in_bag') and a['weight'] <= bag_vol:
            a['in_bag'] = True
            cur = a['value'] + package(apples, bag_vol - a['weight'])
            res = max(res, cur)
            a['in_bag'] = False

    return res


def pay(coin_types: list, product_price: int):
    if product_price == 0:
        return []
    res = None
    for c in coin_types:
        if c <= product_price:
            cur = pay(coin_types, product_price - c)
            if cur is not None:
                cur.append(c)
            if res is None:
                res = cur
            elif cur and len(cur) < len(res):
                res = cur
    return res


def solve_bag_problem(volume, items: list):
    cache = {}

    def inner(vol, i):
        key = (vol, i)
        if key in cache:
            return cache[key]

        if i < 0:
            return 0, set()

        itm = items[i]
        if itm['weight'] <= vol:
            a, a_indexes = inner(vol - itm['weight'], i - 1)
            a += itm['weight']
            a_indexes.add(i)
            b, b_indexes = inner(vol, i - 1)
            r = (a, a_indexes) if a > b else (b, b_indexes)
            cache[key] = r
            return r
        else:
            r = inner(vol, i - 1)
            cache[key] = r
            return r

    res = inner(volume, len(items) - 1)
    res = list(res)

    # print(res)

    res[-1] = [items[i] for i in res[-1]]

    return res


if __name__ == '__main__':
    # coins = [2, 5, 7]
    # print(pay(coins, 9))

    apps = [
               {'value': 50, 'weight': 50},
               {'value': 30, 'weight': 30},
               {'value': 30, 'weight': 30},
           ] * 100

    bag_vol = 15000

    print(solve_bag_problem(bag_vol, apps))
