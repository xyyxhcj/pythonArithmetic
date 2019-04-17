# 双向查询路径,直到路径交汇
from queue import PriorityQueue


def print_path(path, distance):
    print('Path found:%s,distance:%s' % (path, distance))


def bs(graph, origin, dest):
    # 使用优先级排序queue(根据距离排序),存储途经路线list,分为起点队列和终点队列
    origin_queue = PriorityQueue()
    dest_queue = PriorityQueue()
    origin_queue.put((0, [origin]))
    dest_queue.put((0, [dest]))
    # 存储起点/终点到某一点的距离,以空间换时间
    distance_dict = {}
    while not origin_queue.empty() and not dest_queue.empty():
        origin_node = origin_queue.get()
        dest_node = dest_queue.get()
        # 获取两条路线的最后一个地址,如果被包含于另一条路线,则表示已找到,拼接路线
        origin_list = origin_node[1]
        dest_list = dest_node[1]
        origin_last = origin_list[len(origin_list) - 1]
        dest_last = dest_list[len(dest_list) - 1]

        # 仅存储最短距离
        key = origin + '_' + origin_last
        if key not in distance_dict or distance_dict[key] > origin_node[0]:
            distance_dict[key] = origin_node[0]
        key = dest + '_' + dest_last
        if key not in distance_dict or distance_dict[key] > dest_node[0]:
            distance_dict[key] = dest_node[0]
        if origin_last in dest_list:
            # 计算另一方途径点中某段线路的距离 或者在遍历时存储最短途径两点，方便获取
            distance = origin_node[0] + distance_dict[dest + '_' + origin_last]
            print_path(origin_list + dest_list[dest_list.index(origin_last) - 1::-1], distance)
            break
        elif dest_last in origin_list:
            distance = dest_node[0] + distance_dict[origin + '_' + dest_last]
            print_path(origin_list[:origin_list.index(dest_last)] + dest_list[::-1], distance)
            break
        # 将两个城市直达的地址存入queue
        if origin_last in graph:
            for city, distance in graph[origin_last].items():
                if city not in origin_list:
                    origin_queue.put((origin_node[0] + distance, origin_list[:] + [city]))
        if dest_last in graph:
            for city, distance in graph[dest_last].items():
                if city not in dest_list:
                    dest_queue.put((dest_node[0] + distance, dest_list[:] + [city]))


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
    bs(graph, 'Anyang', 'HongKong')
    bs(graph, 'Anyang', 'Shenzhen')
    bs(graph, 'Beijing', 'Xiamen')


if __name__ == '__main__':
    main()
