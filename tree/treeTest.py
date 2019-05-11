# 查前K个高频元素 nlogK
# https://leetcode-cn.com/problems/top-k-frequent-elements/
from typing import List

# class Item:
#
#     def __init__(self, data: int, count=1) -> None:
#         self.data = data
#         self.count = count
#
#     def compare(self, other):
#         return 1 if self.count > other.count else -1


'''
class Tree:

    def __init__(self) -> None:
        self.itemList = []
        self.count = {}

    def set_count(self, num):
        if self.count[num] is None:
            self.
            self.count[num] = 0
        self.count[num] += 1

    def add(self, num, max_size):
        self.set_count(num)
        if len(self.itemList) < max_size:
            # 将元素放到末尾,再整理堆
            self.itemList.append(num)
            self.collating()
        elif self.count[num]>self.count[self.itemList[0]]:
            # 超过存取长度,当计数大于堆顶时,交换堆顶,将原堆顶元素与计数最小的元素交换,取出最小的元素,整理堆
            self.itemList[0],
            
        

    # 整理堆
    def collating(self):
        nums = self.itemList
        length = len(nums)
        # 从最后的父结点倒序遍历
        i = (length - 1) // 2
        while i >= 0:
            # 获取最小的子结点
            child_index = i * 2 + 1
            if child_index + 1 < length and self.count[nums[child_index + 1]] > self.count[nums[child_index]]:
                child_index = child_index + 1
            if self.count[nums[child_index]] > self.count[nums[i]]:
                nums[child_index], nums[i] = nums[i], nums[child_index]
                # 继续从变更后的父结点索引开始整理
                i = (i - 1) // 2
            else:
                # 整理完毕
                break
'''


class Item:
    def __init__(self, data: int, count=1, index=-1) -> None:
        self.data = data
        self.count = count
        self.index = index

    def compare(self, other):
        return 1 if self.count > other.count else -1


# 使用最小堆,即堆顶的元素比较值最小
class Tree:

    def __init__(self) -> None:
        self.itemList = []

    def add(self, item: Item, max_size):
        length = len(self.itemList)
        if length < max_size:
            # 如果未超过最大长度,则将元素放到末尾,再整理堆
            self.itemList.append(item)
            item.index = length - 1
            self.collating(item)
        elif self.itemList[0].count < item.count:
            # 超过存取长度,当计数大于堆顶时,交换堆顶,从上往下整理堆
            self.itemList[0] = item
            self.collating_from_top()

    # 整理堆
    def collating(self, item):
        nums = self.itemList
        length = len(nums)
        # 从item结点开始倒序遍历
        i = item.index
        if i == -1 and item.count > nums[0].count:
            # 未在堆中,当比较值比堆顶元素大时,替换,从堆顶往下整理堆
            self.itemList[0] = item
            self.collating_from_top()
        else:
            while i >= 0:
                # 获取最小的子结点
                child_index = i * 2 + 1
                if child_index >= length:
                    # 越界时从当前结点的父结点继续整理
                    i = (i - 1) // 2
                    continue
                if child_index + 1 < length and nums[child_index + 1].count < nums[child_index].count:
                    child_index = child_index + 1
                if nums[child_index].count < nums[i].count:
                    nums[child_index], nums[i] = nums[i], nums[child_index]
                    # 设置变更后的索引
                    nums[child_index].index, nums[i].index = child_index, i
                    # 继续从变更后的父结点索引开始整理
                    i = (i - 1) // 2
                else:
                    # 整理完毕
                    break

    def collating_from_top(self):
        i = 0
        nums = self.itemList
        length = len(nums)
        # 遍历所有父结点
        while i < (length - 2) // 2:
            # 获取最小的子结点
            child_index = i * 2 + 1
            if child_index + 1 < length and nums[child_index + 1].count < nums[child_index].count:
                child_index = child_index + 1
            if nums[child_index].count < nums[i].count:
                nums[child_index], nums[i] = nums[i], nums[child_index]
                # 设置变更后的索引
                nums[child_index].index, nums[i].index = child_index, i
                # 继续从变更后的子结点索引开始整理
                i = child_index
            else:
                # 整理完毕
                break

    def get_result(self) -> List[int]:
        return [item.data for item in self.itemList]


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        tree = Tree()
        # 把所有数字放入字典,数字:item{数字,位置,个数};同时放入元素上限为k的堆中
        item_count = {}
        for num in nums:
            if num not in item_count:
                item = Item(num)
                item_count[num] = item
                # 放入堆
                tree.add(item, k)
            else:
                item_count[num].count += 1
                # 触发堆重新排序
                tree.collating(item_count[num])
        return tree.get_result()


print(Solution().topKFrequent([1, 1, 1, 2, 2, 3], 2))
