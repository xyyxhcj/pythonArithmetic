class NumArray(object):

    def __init__(self, nums):
        """
        :type nums: List[int]
        """
        # 遍历,在每个结点中存储索引0到当前索引的和
        self.nums = nums
        total = 0
        self.totals = []
        for num in nums:
            total += num
            self.totals.append(total)

    def sumRange(self, i, j):
        """
        :type i: int
        :type j: int
        :rtype: int
        """
        return self.totals[j] - self.totals[i] + self.nums[i]


if __name__ == '__main__':
    print(NumArray([-2, 0, 3, -5, 2, -1]).sumRange(0, 2))
    print(NumArray([-2, 0, 3, -5, 2, -1]).sumRange(2, 5))
    print(NumArray([-2, 0, 3, -5, 2, -1]).sumRange(0, 5))
    print(NumArray([]))
