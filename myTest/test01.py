# 一个长度为1000的数组，它的值在1~99之间，如何按值在数组中出现的次数从高到低排列
import random

if __name__ == '__main__':
    arr = [random.randint(1, 99) for i in range(1000)]
    count_dict = dict()
    for x in arr:
        count = count_dict.get(x, 0)
        count_dict[x] = count + 1
    arr = [[] for i in range(1000)]
    for k, v in count_dict.items():
        arr[v].append(k)
    for i in range(999, -1, -1):
        if len(arr[i]) > 0:
            print('出现次数：%d,值：%s,size：%d' % (i, arr[i], len(arr[i])))
