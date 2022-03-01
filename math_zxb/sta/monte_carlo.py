import math
import random
from collections import Counter
from typing import Callable, List
import matplotlib.pyplot as plt

def sampling(sample_func:Callable[[],float],n:int,sta_func:Callable[[List],float]):
    return sta_func([sample_func() for i in range(n)])


def hist(xs:List[float]):
    # m=math.ceil(math.log2(len(xs)))
    # lo=min(xs)
    # hi=max(xs)
    # delta=(hi-lo)/m
    #
    # res=Counter([(x-lo)//delta for x in xs])
    #
    # res2=[(lo+k*delta,v) for k,v in res.items()]
    #
    # plt.plot([x[0] for x in res2],[x[1] for x in res2])
    plt.hist(xs,bins=math.ceil(math.log2(len(xs)))*2)
    plt.show()


if __name__=='__main__':
    sample_func=random.random

    res=[sampling(sample_func,12800,lambda x:sum(x)/len(x)) for i in range(10000)]

    hist(res)

