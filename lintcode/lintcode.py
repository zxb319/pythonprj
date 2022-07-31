class Solution:
    """
    @param s: A string with lowercase letters and parentheses
    @return: A string which has been removed invalid parentheses
    """
    def remove_parentheses(self, s: str) -> str:
        # write your code here.
        res=[]
        cur=0
        for c in s:
            if c!=')':
                res.append(c)
                if c=='(':
                    cur+=1
            elif c==')':
                if cur>0:
                    cur-=1
                    res.append(c)

        res2=[]
        cur=0
        for c in reversed(res):
            if c!='(':
                res2.append(c)
                if c==')':
                    cur+=1
            elif c=='(':
                if cur>0:
                    cur-=1
                    res2.append(c)

        return ''.join(c for c in reversed(res2))
