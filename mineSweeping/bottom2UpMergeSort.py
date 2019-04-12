# 自底向上的归并排序
import random


def merge_sort(arr, start, middle, end):
    length = len(arr)
    if middle - start >= length:
        return length
    end = end if length > end else length
    l_1, l_2 = arr[start:middle], arr[middle:end]
    # 添加哨兵牌
    l_1.append(float('inf'))
    l_2.append(float('inf'))
    i_1, i_2 = 0, 0
    for i in range(start, end):
        if l_1[i_1] < l_2[i_2]:
            arr[i] = l_1[i_1]
            i_1 += 1
        else:
            arr[i] = l_2[i_2]
            i_2 += 1
    return end - start


def marge(arr):
    # 从单个元素开始不断归并,直到两个子序列归并的长度等于总长度时停止归并
    marge_length = 0
    step = 1
    while True:
        if marge_length == len(arr):
            break
        step *= 2
        for i in range(0, len(arr), step):
            marge_length = merge_sort(arr, i, (i + i + step) // 2, i + step)


def main():
    arr = []
    # 初始化随机数组
    for i in range(10):
        randint = random.randint(0, 30)
        arr.append(randint)
    print(arr)
    marge(arr)
    print(arr)


if __name__ == '__main__':
    main()
