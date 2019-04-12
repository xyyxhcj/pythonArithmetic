# 测试随机洗牌算法概率
import random

HIT_VALUE = 1


# 洗牌方法,返回命中次数数组
# 将每个元素置换len(arr)次
def shuffle1(arr, hits, num):
    for i in range(num):
        for j in range(len(arr)):
            a = random.randint(0, len(arr) - 1)
            b = random.randint(0, len(arr) - 1)
            arr[a], arr[b] = arr[b], arr[a]
        # 统计命中次数
        count_hits(arr, hits)


# 仅置换有元素的区域
def shuffle2(arr, hits, num):
    for i in range(num):
        for j in range(10):
            a = random.randint(0, len(arr) - 1)
            arr[a], arr[j] = arr[j], arr[a]
        # 统计命中次数
        count_hits(arr, hits)


def fisher_yates_shuffle(arr, hits, num):
    for i in range(num):
        for j in range(len(arr) - 1, 0, -1):
            # 获取0-j之前的随机元素与j转换
            randint = random.randint(0, j - 1)
            arr[randint], arr[j] = arr[j], arr[randint]
        # 统计命中次数
        count_hits(arr, hits)


def count_hits(arr, hits):
    for k in range(len(arr)):
        if arr[k] == HIT_VALUE:
            hits[k] += 1


def show(hits, num):
    for hit in hits:
        print(hit / num)


def main():
    # 待洗牌数组
    arr = []
    # 命中次数
    hits = []
    for i in range(10):
        arr.append(-1)
        hits.append(0)
    for i in range(5):
        arr[i] = HIT_VALUE
    # 洗牌之后,每个元素结果为1的概率应为50%
    times = 100000
    # shuffle1(arr, hits, times)
    # shuffle2(arr, hits, times)
    fisher_yates_shuffle(arr, hits, times)
    show(hits, times)


if __name__ == '__main__':
    main()
