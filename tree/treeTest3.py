# 查前K个高频元素 nlogK
# https://leetcode-cn.com/problems/top-k-frequent-elements/
from typing import List


# 使用最小堆,即堆顶的元素比较值最小
class Tree:

    def __init__(self, item_count) -> None:
        self.item_count = item_count
        self.itemList = []

    # 整理堆
    def collating(self, start):
        item_count = self.item_count
        nums = self.itemList
        length = len(nums)
        # 遍历所有父结点
        while start <= (length - 2) >> 1:
            # 获取最小的子结点
            child_index = start * 2 + 1
            if child_index + 1 < length and item_count[nums[child_index + 1]] < item_count[nums[child_index]]:
                child_index = child_index + 1
            if item_count[nums[child_index]] < item_count[nums[start]]:
                nums[child_index], nums[start] = nums[start], nums[child_index]
                # 继续从变更后的子结点索引开始整理
                start = child_index
            else:
                # 整理完毕
                break

    # 从底向上遍历整理
    def collating2top(self, start):
        item_count = self.item_count
        nums = self.itemList
        # 遍历所有父结点
        while start > 0:
            # 获取父结点
            parent_index = (start - 1) >> 1
            if item_count[nums[parent_index]] > item_count[nums[start]]:
                nums[parent_index], nums[start] = nums[start], nums[parent_index]
                # 继续从变更后的子结点索引开始整理
                start = parent_index
            else:
                # 整理完毕
                break

    def get_result(self, max_size) -> List[int]:
        for key, v in self.item_count.items():
            length = len(self.itemList)
            if length < max_size:
                self.itemList.append(key)
                self.collating2top(length)
            elif v > self.item_count[self.itemList[0]]:
                self.itemList[0] = key
                self.collating(0)
        return self.itemList


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # 把所有数字放入字典,数字:个数
        item_count = dict()
        for num in nums:
            item_count[num] = 1 if num not in item_count.keys() else item_count[num] + 1
        return Tree(item_count).get_result(k)


# [-4, 0, 1, 4, 9, -3]
print(Solution().topKFrequent([6, 0, 1, 4, 9, 7, -3, 1, -4, -8, 4, -7, -3, 3, 2, -3, 9, 5, -4, 0], 6))
