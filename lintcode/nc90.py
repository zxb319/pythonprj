

class Solution:
    def __init__(self):
        self._data=[]
        self._mins=[]

    def push(self, node):
        # write code here
        self._data.append(node)
        if not self._mins or node<=self._mins[-1]:
            self._mins.append(node)

    def pop(self):
        # write code here
        res=self._data.pop(len(self._data)-1)
        if res==self._mins[-1]:
            self._mins.pop(len(self._mins)-1)

    def top(self):
        # write code here
        return self._data[-1]

    def min(self):
        # write code here
        return self._mins[-1]