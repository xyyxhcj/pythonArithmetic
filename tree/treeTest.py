# 查前K个高频元素 nlogK
# https://leetcode-cn.com/problems/top-k-frequent-elements/
from typing import List


class Item:

    def __init__(self, data: int) -> None:
        self.data = data

    def compare(self, other):
        return 1 if self.data > other.data else -1


class Tree:

    def __init__(self, root) -> None:
        self.root = root
        self.left = self.right = None

    def add(self, item):
        stack = [self.root]
        pop = stack.pop()
        # 最大堆,将最大的数据放在堆顶
        while pop.data != None:
            if item.compare(pop) == 1:
                pop.data = item.data

        self.item = item


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # stack=stack
        # 遍历,放入最小堆
        for num in nums:
            pass
