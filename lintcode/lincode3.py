import math_zxb.zxb


def solve(formula:str,lo,hi):
    def inner(x):
        return eval(formula,{},locals())

    return math_zxb.zxb.root_binarily(inner,lo,hi)


if __name__ == '__main__':
    a=solve('5*x+1-4.9*(x+1)',0,100)
    print(a)