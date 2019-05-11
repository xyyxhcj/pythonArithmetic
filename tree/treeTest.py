# 查前K个高频元素 nlogK
# https://leetcode-cn.com/problems/top-k-frequent-elements/
from typing import List


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
			item.index = length
			self.collating(item)
		elif item.count > self.itemList[0].count:
			# 超过存取长度,当计数大于堆顶时,拿掉堆顶元素,从上往下整理堆
			self.itemList[0].index = -1
			self.itemList[0] = item
			item.index = 0
			self.collating_from_top()

	# 整理堆
	def collating(self, item):
		nums = self.itemList
		length = len(nums)
		# 从item结点开始倒序遍历
		i = item.index
		if i == -1 and item.count > nums[0].count:
			# 未在堆中,当比较值比堆顶元素大时,拿掉堆顶元素,从堆顶往下整理堆
			nums[0].index = -1
			nums[0] = item
			item.index = 0
			self.collating_from_top(item)
		elif i != -1:
			self.collating_from_top(item)

	def collating_from_top(self, item):
		start = item.index
		nums = self.itemList
		length = len(nums)
		# 遍历所有父结点
		while start <= (length - 2) >> 1:
			# 获取最小的子结点
			child_index = start * 2 + 1
			if child_index + 1 < length and nums[child_index + 1].count < nums[child_index].count:
				child_index = child_index + 1
			if nums[child_index].count < nums[start].count:
				nums[child_index], nums[start] = nums[start], nums[child_index]
				# 设置变更后的索引
				nums[child_index].index, nums[start].index = child_index, start
				# 继续从变更后的子结点索引开始整理
				start = child_index
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

