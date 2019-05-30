from typing import List


class NumArray:

    def __init__(self, nums: List[int]):
        self.nums = [{'data': num} for num in nums]
        # 创建线段树
        self.tree = [0 for n in range(len(nums) * 4)]
        self.buildSegmentTree(0, 0, len(nums) - 1)

    def update(self, i: int, val: int) -> None:
        temp = val - self.nums[i]['data']
        self.nums[i]['data'] = val
        tree_index = self.nums[i]['t_index']
        # 更新父结点的值
        self.update_parent(temp, tree_index)

    def update_parent(self, temp, tree_index):
        if temp != 0:
            while tree_index >= 0:
                self.tree[tree_index] += temp
                tree_index = (tree_index - 1) // 2

    def sumRange(self, i: int, j: int) -> int:
        return self.query(0, 0, len(self.nums) - 1, i, j)

    def buildSegmentTree(self, tree_index: int, l_index: int, r_index: int):
        if l_index > r_index:
            return
        if l_index == r_index:
            self.tree[tree_index] = self.nums[l_index]['data']
            self.nums[l_index]['t_index'] = tree_index
            return
        mid = (l_index + r_index) >> 1
        l_child = (tree_index << 1) + 1
        r_child = l_child + 1
        self.buildSegmentTree(l_child, l_index, mid)
        self.buildSegmentTree(r_child, mid + 1, r_index)
        self.tree[tree_index] = self.tree[l_child] + self.tree[r_child]

    def query(self, tree_index, l_index, r_index, query_l, query_r):
        if l_index == r_index or (l_index == query_l and r_index == query_r):
            return self.tree[tree_index]
        l_child = (tree_index << 1) + 1
        r_child = l_child + 1
        mid = (l_index + r_index) >> 1
        if mid < query_l:
            return self.query(r_child, mid + 1, r_index, query_l, query_r)
        elif mid >= query_r:
            return self.query(l_child, l_index, mid, query_l, query_r)
        else:
            # 数据分布在左子树与右子树间
            return self.query(l_child, l_index, mid, query_l, mid) + self.query(r_child, mid + 1, r_index, mid + 1,
                                                                                query_r)


if __name__ == '__main__':
    array = NumArray([1, 3, 5])
    print(array.sumRange(0, 2))
    array.update(1, 2)
    print(array.sumRange(0, 2))
    print('-' * 9)
    array = NumArray([0, 9, 5, 7, 3])
    print(array.sumRange(4, 4))
    print(array.sumRange(2, 4))
    print(array.sumRange(3, 3))
    array.update(4, 5)
    array.update(1, 7)
    array.update(0, 8)
    print(array.sumRange(1, 2))
    array.update(1, 9)
    print(array.sumRange(4, 4))
    array.update(3, 4)
