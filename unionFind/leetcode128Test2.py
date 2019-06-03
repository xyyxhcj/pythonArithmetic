from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        length_count = dict()
        max_count = 0
        for num in nums:
            if num in length_count:
                # 忽略重复值
                continue
            left_count = length_count.get(num - 1, 0)
            right_count = length_count.get(num + 1, 0)
            # 每个元素的序列长度=比元素小1的序列长度+比元素大1的序列长度+1
            count = left_count + right_count + 1
            length_count[num] = count
            # 对当前序列的首尾元素及当前元素赋值,防止重复计算
            length_count[num] = count
            length_count[num - left_count] = count
            length_count[num + right_count] = count
            if max_count < count:
                max_count = count
        return max_count


if __name__ == '__main__':
    print(Solution().longestConsecutive([1, 3, 5, 2, 4]))
    print(Solution().longestConsecutive([0, 0, -1]))
