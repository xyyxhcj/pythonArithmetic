from typing import List


class NumArray:

    def __init__(self, nums: List[int]):
        self.nums = nums
        self.total = 0
        self.count_total = [self.sum(num) for num in nums]

    def update(self, i: int, val: int) -> None:
        temp = val - self.nums[i]
        self.nums[i] = val
        if temp != 0:
            for k in range(i, len(self.count_total), 1):
                self.count_total[k] += temp

    def sumRange(self, i: int, j: int) -> int:
        return self.count_total[j] if i == 0 else self.count_total[j] - self.count_total[i - 1]

    def sum(self, num):
        self.total += num
        return self.total


# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# obj.update(i,val)
# param_2 = obj.sumRange(i,j)

if __name__ == '__main__':
    array = NumArray([1, 3, 5])
    print(array.sumRange(0, 2))
    array.update(1, 2)
    print(array.sumRange(0, 2))
