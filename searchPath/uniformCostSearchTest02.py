# 单向搜索路径
from queue import PriorityQueue


def ucs(graph, origin, dest):
    # 使用优先级排序queue(根据距离排序),存储途经路线list
    queue = PriorityQueue()
    queue.put((0, [origin]))
    while not queue.empty():
        node = queue.get()
        # 获取路线的最后一个地址
        city_list = node[1]
        last_city = city_list[len(city_list) - 1]
        if last_city == dest:
            print('Path found:%s,distance:%s' % (node[1], node[0]))
            break
        # 查询当前城市的可直达城市,存入队列
        if last_city in graph:
            for city, distance in graph[last_city].items():
                if city in city_list:
                    # 如果已途径该城市,则跳过
                    continue
                queue.put((node[0] + distance, city_list[:] + [city]))


def main():
    f = open('maps.txt')
    # 存入dict
    graph = {}
    for line in f.readlines():
        nodes = line.split()
        key = nodes[0]
        value = {}
        for i in range(1, len(nodes), 2):
            value[nodes[i]] = int(nodes[i + 1])
        graph[key] = value
    print('graph:%s' % graph)
    ucs(graph, 'Anyang', 'HongKong')
    ucs(graph, 'Xiamen', 'Shenzhen')
    ucs(graph, 'Beijing', 'Xiamen')


if __name__ == '__main__':
    main()
