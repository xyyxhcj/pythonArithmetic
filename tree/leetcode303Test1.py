class NumArray(object):

    def __init__(self, nums):
        """
        :type nums: List[int]
        """
        # 构建线段树,每个节点存储下级元素之和
        self.tree = [None for i in range(len(nums) * 4)]
        self.nums = nums
        self.build_segment_tree(0, 0, len(nums) - 1)

    def sumRange(self, i, j):
        """
        :type i: int
        :type j: int
        :rtype: int
        """
        return self.query(0, 0, len(self.nums) - 1, i, j)

    def build_segment_tree(self, tree_index, left_index, right_index):
        if left_index > right_index:
            return
        if left_index == right_index:
            print(tree_index)
            print(left_index)
            print(right_index)
            self.tree[tree_index] = self.nums[left_index]
            return
        # 以中点切割，裂变
        mid = (left_index + right_index) // 2
        left_child_index = tree_index * 2 + 1
        right_child_index = tree_index * 2 + 2
        self.build_segment_tree(left_child_index, left_index, mid)
        self.build_segment_tree(right_child_index, mid + 1, right_index)
        if self.tree[tree_index] is None:
            self.tree[tree_index] = self.tree[left_child_index] + self.tree[right_child_index]

    def query(self, tree_index, l_index, r_index, query_l, query_r):
        if l_index == query_l and r_index == query_r:
            return self.tree[tree_index]
        mid = (l_index + r_index) // 2
        l_child = tree_index * 2 + 1
        r_child = tree_index * 2 + 2
        if query_l <= mid < query_r:
            # 表示结果分布于两个子树
            return self.query(l_child, l_index, mid, query_l, mid) + self.query(r_child, mid + 1, r_index, mid + 1,
                                                                                query_r)
        elif query_r <= mid:
            # 结果只分布在左子树
            return self.query(l_child, l_index, mid, query_l, query_r)
        else:
            # query_l > mid 结果只分布在右子树
            return self.query(r_child, mid + 1, r_index, query_l, query_r)


if __name__ == '__main__':
    print(NumArray([-2, 0, 3, -5, 2, -1]).sumRange(0, 2))
    print(NumArray([-2, 0, 3, -5, 2, -1]).sumRange(2, 5))
    print(NumArray([-2, 0, 3, -5, 2, -1]).sumRange(0, 5))
    print(NumArray([]))
