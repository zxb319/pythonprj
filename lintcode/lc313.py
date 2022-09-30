import copy
from typing import List


class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        res=[1 if nums[0]==1 else -1]
        for i in range(1,len(nums)):
            c=nums[i]
            

class Solution:
    def longestWPI(self, hours: List[int]) -> int:
        lwpi=[1 if hours[0]>8 else -1]
        for i in range(1,len(hours)):
            h=hours[i]
            c=1 if h>8 else -1
            lwpi.append(max(lwpi[-1],0)+c)

        return max(max(lwpi),0)


