import math

from math_zxb import integral


class LogNormalDistribution:
    def __init__(self,alpha:float,beta:float):
        self._alpha=alpha
        self._beta=beta

        def f(x:float):
            t1=1/(2*math.pi)**0.5/self._beta
            t2=math.e**(-(math.log(x,math.e)-self._alpha)**2/2/self._beta**2)
            return t1*t2/x

        self._df=f

    def cp(self,x:float):
        return integral(self._df,0.0000001,x)


if __name__=='__main__':
    pd=LogNormalDistribution(0,1)
    print(pd.cp(1))