class Solution:
    """
    @param n: A long integer
    @return: An integer, denote the number of trailing zeros in n!
    """
    def trailingZeros(self, n: int) -> int:
        # write your code here
        res=0
        while n>0:
            n//=5
            res+=n

        return res


if __name__=='__main__':
    res=1
    for i in range(1,200+1):
        res*=i
        print(i,res,Solution().trailingZeros(i))