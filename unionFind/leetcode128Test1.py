from typing import List


# 并查集
class UnionFind:

    def __init__(self, nums) -> None:
        self.father = [{'father': i, 'level': 0, 'count': 1} for i in range(len(nums))]

    def union(self, x, y):
        x_father = self.get_father(x)
        y_father = self.get_father(y)
        if x_father != y_father:
            if x_father['level'] < y_father['level']:
                y_father['count'] += x_father['count']
                self.father[x_father['father']] = y_father
            elif x_father['level'] > y_father['level']:
                x_father['count'] += y_father['count']
                self.father[y_father['father']] = x_father
            else:
                y_father['count'] += x_father['count']
                self.father[x_father['father']] = y_father
                y_father['level'] += 1

    def get_father(self, x):
        father = x
        while father != self.father[father]['father']:
            father = self.father[father]['father']
        return self.father[father]


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        # 以值为key,索引为value,生成字典
        nums = list(set(nums))
        data = {nums[i]: i for i in range(len(nums))}
        union_find = UnionFind(nums)
        for i in range(len(nums)):
            num = nums[i]
            # 判断是否有比该元素小1的数据,有则连接
            if num - 1 in data:
                # 连结
                union_find.union(i, data[num - 1])
        # 计数
        max_length = 0
        for i in range(len(nums)):
            father = union_find.get_father(i)
            if father['count'] > max_length:
                max_length = father['count']
        return max_length


if __name__ == '__main__':
    print(Solution().longestConsecutive([1, 3, 5, 2, 4]))
    print(Solution().longestConsecutive([0, 0, -1]))
