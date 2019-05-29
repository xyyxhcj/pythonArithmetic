# 查前K个高频元素 使用索引列表 时间复杂度O(n)
# https://leetcode-cn.com/problems/top-k-frequent-elements/
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # 把所有数字放入字典,数字:个数
        num_count = dict()
        for num in nums:
            num_count[num] = num_count.get(num, 0) + 1
        arr = []
        sort_list = [None for i in range(len(nums) + 1)]
        for key, val in num_count.items():
            if sort_list[val] is None:
                sort_list[val] = []
            sort_list[val].append(key)
        for i in range(len(sort_list) - 1, -1, -1):
            if len(arr) == k:
                break
            if sort_list[i] is not None:
                arr += sort_list[i]
        return arr


# [-4, 0, 1, 4, 9, -3]
print(Solution().topKFrequent([6, 0, 1, 4, 9, 7, -3, 1, -4, -8, 4, -7, -3, 3, 2, -3, 9, 5, -4, 0], 6))

