import os


def factors(num: int):
    if num < 0:
        raise ArithmeticError("num must >0")

    if num <= 1:
        return {num: 1}

    res = {}
    while num > 1:
        f = 2
        while f <= num:
            if num % f == 0:
                res[f] = res.get(f, 0) + 1
                num //= f
                break

            f += 1

    return res


def lcm(a: int, b: int):
    """最小公倍数"""
    return a // gcd(a, b) * b


def wander_files(path: str):
    if not os.path.exists(path):
        raise Exception(rf'path: {path} do not exists.')
    cur={
        'name':os.path.basename(path),
        'size':os.stat(path).st_size,
        'children':None
    }
    if os.path.isdir(path):
        cur['children']=[]
        cur['size']=0
        for cname in os.listdir(path):
            cur_child=wander_files(os.path.join(path,cname))
            cur['children'].append(cur_child)
            cur['size']+=cur_child['size']

    return cur


def gcd(a: int, b: int) -> int:
    while a != 0:
        newa = b % a
        b = a
        a = newa

    return b


def fib():
    f0 = 0
    f1 = 1
    yield f0
    yield f1
    while True:
        f1 += f0
        f0 = f1 - f0
        yield f1


def isPrime(num: int) -> bool:
    if num < 2: return False
    i = 2
    while i * i <= num:
        if num % i == 0:
            return False
        i += 1

    return True


if __name__ == "__main__":
    files=wander_files(r'd:\weiyun\pythonprj\dsa')
    import json
    print(json.dumps(files))
