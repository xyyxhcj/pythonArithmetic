class Solution:
    def longestConsecutive(self, nums):
        # 记录最长序列
        longest_sequence = 0
        num_set = {num for num in nums}
        for num in nums:
            if num - 1 not in num_set:
                # 仅对一个序列中的最小元素进行穷举，获取序列长度
                sequence = 1
                while num + 1 in num_set:
                    num += 1
                    sequence += 1
                if sequence > longest_sequence:
                    longest_sequence = sequence
        return longest_sequence


if __name__ == '__main__':
    print(Solution().longestConsecutive([1, 3, 5, 2, 4]))
    print(Solution().longestConsecutive([0, 0, -1]))
