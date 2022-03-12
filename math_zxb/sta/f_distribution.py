import math

import math_zxb
from math_zxb.sta.distributions import Dist


class FDistribution(Dist):
    def __init__(self,m:int,n:int):
        self._m=m
        self._n=n

        gamma_mn2=math.gamma((m+n)/2)
        fenmu=math.gamma(m/2)*math.gamma(n/2)

        def f(x:float):
            if x==0.0:
                return 0
            a=gamma_mn2*m**(m/2)*n**(n/2)*x**(m/2-1)*(n+m*x)**(-(m+n)/2)
            if isinstance(a,complex):
                print(m,n,x)
                raise ArithmeticError('a is complex')
            # a=math.gamma((m+n)/2)*(m/n)**(m/2)*x**(m/2-1)*(1+m/n*x)**(-(m+n)/2)
            return a/fenmu

        self._pdf=f


    def cp(self,x:float):
        assert x>=0
        return math_zxb.integral(self._pdf,0.00001,x)

    def pbetween(self,lo:float,hi:float):
        assert lo<=hi
        return math_zxb.integral(self._pdf,lo,hi)

    def x_of(self,p:float):
        assert 0<p<1
        return math_zxb.root_binarily(lambda x:self.cp(x)-p,0.00001,1000)

    def range_of(self,p:float):
        lo=math_zxb.root_binarily(lambda x:self.cp(x)-(1-p)/2,1e-5,1000)
        hi=math_zxb.root_binarily(lambda x:self.cp(x)-(1+p)/2,1e-5,1000)

        return lo,hi


if __name__=='__main__':
    pd=FDistribution(1,10)
    print(pd.x_of(0.95))



