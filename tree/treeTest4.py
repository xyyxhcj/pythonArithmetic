# 查前K个高频元素 nlogK
# https://leetcode-cn.com/problems/top-k-frequent-elements/
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # 把所有数字放入字典,数字:个数
        num_count = dict()
        for num in nums:
            num_count[num] = num_count.get(num, 0) + 1
        arr = sorted(num_count, key=num_count.__getitem__, reverse=True)
        return arr[:k]


# [-4, 0, 1, 4, 9, -3]
print(Solution().topKFrequent([6, 0, 1, 4, 9, 7, -3, 1, -4, -8, 4, -7, -3, 3, 2, -3, 9, 5, -4, 0], 6))
