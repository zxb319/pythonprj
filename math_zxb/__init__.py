import random
import math
from typing import Callable

import numba

import dsa.run_time


def differential(f: Callable[[float], float], x: float):
    delta = 0.0000001
    return (f(x + delta) - f(x)) / delta


def integral(func: Callable[[float], float], lo: float, hi: float):
    n = 100_0000
    delta = (hi - lo) / n
    res = 0
    for i in range(n):
        res += (func(lo + delta * (i)) + func(lo + delta * (i + 1))+4*func(lo+delta*(i+0.5))) / 6 * delta

    return res


def root_binarily(func: Callable[[float], float], lo: float, hi: float):
    if lo > hi:
        raise ArithmeticError("lo<=hi is must.")

    flo = func(lo)
    fhi = func(hi)
    if flo * fhi > 0:
        print(lo,flo,hi,fhi)
        raise ArithmeticError(f"func(lo)*func(hi)<=0 is must.lo={lo},hi={hi}")

    while True:
        mi = (lo + hi) / 2
        if mi in (lo, hi):
            return hi

        fmi = func(mi)
        if flo * fmi <= 0:
            hi = mi
        else:
            lo = mi
            flo = fmi


@dsa.run_time.run_time
def particle_swarm_optimize(func:Callable,start_area):
    particles_count=10000
    iteration_count=100
    positions=[[x[0]+random.random()*(x[1]-x[0]) for x in start_area] for i in range(particles_count)]
    local_optimimals=[p for p in positions]
    global_optimal=min(local_optimimals,key=lambda x:func(x))
    speeds=[[0]*len(start_area) for i in range(particles_count)]
    for i in range(iteration_count):
        speeds=[[vi+random.random()*(poi-ppi)+random.random()*(go-ppi) for vi,poi,ppi,go in zip(v,po,pp,global_optimal)]
               for v,po,pp in zip(speeds,local_optimimals,positions)]

        positions=[[ppi+speedi for ppi,speedi in zip(pp,speed)] for pp,speed in zip(positions,speeds)]

        local_optimimals=[min((lo,pp),key=lambda x:func(x)) for lo,pp in zip(local_optimimals,positions)]
        global_optimal=min(local_optimimals,key=lambda x:func(x))

    return global_optimal


if __name__ == '__main__':

    def f5(x):
        if sum(a*a for a in x)>8:
            return math.inf
        return -sum(a*b for a,b in zip(x,[1,1]))
    res=particle_swarm_optimize(f5,[[0,1]]*2)
    print(res)