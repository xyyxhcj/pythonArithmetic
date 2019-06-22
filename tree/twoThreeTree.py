# 二三树
import random
import tkinter

import math

CONSTANT = {
    'LESS': -1,
    'GREATER': 1,
    'MIDDLE': 0,
    'LEFT': 2,
    'RIGHT': 3
}


class Node:
    def __init__(self, data):
        self.data = data
        self.count = 1

    def compare(self, other) -> int:
        if self.data < other.data:
            return -1
        elif self.data > other.data:
            return 1
        else:
            return 0

    def __str__(self) -> str:
        return str(self.data)


class TreeNode:

    def __init__(self, node: Node, parent=None):
        # 存储父结点引用
        self.parent = parent
        self.nodes = []
        if node is not None:
            self.nodes.append(node)
        self.child_list = [None] * 4

    def compare(self, other: Node):
        compare = self.nodes[0].compare(other)
        # compare = other.compare(self.nodes[0])
        if compare == 1:
            # 第一个结点大于新结点
            return CONSTANT['GREATER']
        elif compare == 0:
            return CONSTANT['LEFT']
        elif len(self.nodes) == 1:
            # 第一个结点小于新结点，无第二个结点
            return CONSTANT['LESS']
        compare = self.nodes[1].compare(other)
        # compare = other.compare(self.nodes[1])
        if compare == -1:
            # 第二个结点小于新结点
            return CONSTANT['LESS']
        elif compare == 0:
            return CONSTANT['RIGHT']
        else:
            # 第二个结点大于新结点
            return CONSTANT['MIDDLE']

    def __str__(self) -> str:
        return str(self.nodes) + '--' + str(self.child_list)

        # 以前序遍历的方式将节点放入list

    def push_arr(self, parent=None, sub_type=None, tree_level=1) -> list:
        self.parent = parent
        self.sub_type = sub_type
        self.tree_level = tree_level
        arr = [self]
        for i in range(3):
            if self.child_list[i] is not None:
                arr += self.child_list[i].push_arr(self, i, tree_level + 1)
        return arr


class TwoThreeTree:

    def __init__(self) -> None:
        self.root = None
        self.size = 0

    def add_node(self, node: Node):
        self.size += 1
        if self.root is None:
            self.root = TreeNode(node)
        else:
            self.root = self.__add_node(self.root, node)
            # if len(self.root.nodes) > 2:
            #     # 拆分结点 两层->三层 todo 画图
            #     self.root = self.split_tree_node(self.root)

    @staticmethod
    def split_tree_node(tree_node: TreeNode) -> TreeNode:
        tree_node_t = TreeNode(tree_node.nodes[1], tree_node.parent)
        tree_node_t.child_list = [TreeNode(tree_node.nodes[0], tree_node_t), TreeNode(tree_node.nodes[2], tree_node_t),
                                  None, None]
        tree_node_t.child_list[0].child_list = [tree_node.child_list[0], tree_node.child_list[1], None, None]
        tree_node_t.child_list[1].child_list = [tree_node.child_list[2], tree_node.child_list[3], None, None]
        if tree_node.child_list[0] is not None:
            tree_node.child_list[0].parent = tree_node.child_list[1].parent = tree_node_t.child_list[0]
            tree_node.child_list[2].parent = tree_node.child_list[3].parent = tree_node_t.child_list[1]
        return tree_node_t

    def __add_node(self, tree_node: TreeNode, node: Node, compare=None, parent=None) -> TreeNode:
        # 如果 tree_node为None,则将node融入父结点
        if tree_node is None:
            compare_index = {CONSTANT['LESS']: 2, CONSTANT['MIDDLE']: 1, CONSTANT['GREATER']: 0}
            parent.nodes.insert(compare_index[compare], node)
            return parent
        else:
            # 比较结点，向匹配的方向插入，获取返回的父结点，当前结点最多只为三结点
            compare_tree_node = tree_node.compare(node)
            if CONSTANT['LESS'] == compare_tree_node:
                if len(tree_node.nodes) == 1:
                    tree_node = self.__add_node(tree_node.child_list[1], node, compare_tree_node, tree_node)
                else:
                    tree_node = self.__add_node(tree_node.child_list[2], node, compare_tree_node, tree_node)
            elif CONSTANT['MIDDLE'] == compare_tree_node:
                tree_node = self.__add_node(tree_node.child_list[1], node, compare_tree_node, tree_node)
            elif CONSTANT['GREATER'] == compare_tree_node:
                tree_node = self.__add_node(tree_node.child_list[0], node, compare_tree_node, tree_node)
            elif CONSTANT['LEFT'] == compare_tree_node:
                tree_node.nodes[0].count += 1
                return tree_node if parent is None else tree_node.parent
            else:
                tree_node.nodes[1].count += 1
                return tree_node if parent is None else tree_node.parent
            if len(tree_node.nodes) > 2:
                # 如果返回的父结点变成三元素，则拆分结点
                tree_node = self.split_tree_node(tree_node)
                if len(tree_node.nodes) == 1 and parent is not None:
                    # 返回的为拆分后的父结点，与上一级继续融合
                    tree_node.parent = self.merge(tree_node.parent.compare(tree_node.nodes[0]), tree_node)
        if parent is None:
            return tree_node
        else:
            return tree_node.parent

    # 合并
    @staticmethod
    def merge(compare, tree_node) -> TreeNode:
        # 将子结点与父结点合并,返回父结点
        parent = tree_node.parent
        if parent is not None:
            if CONSTANT['LESS'] == compare:
                # 新结点大于父结点
                length = len(parent.nodes)
                parent.nodes.append(tree_node.nodes[0])
                if length == 1:
                    # 父结点为双结点,新子结点放入 1 2索引位置
                    parent.child_list[1] = tree_node.child_list[0]
                    parent.child_list[1].parent = parent
                    parent.child_list[2] = tree_node.child_list[1]
                    parent.child_list[2].parent = parent
                else:
                    # 父结点为三结点,新子结点放入 2 3索引位置
                    parent.child_list[2] = tree_node.child_list[0]
                    parent.child_list[2].parent = parent
                    parent.child_list[3] = tree_node.child_list[1]
                    parent.child_list[3].parent = parent
            elif CONSTANT['GREATER'] == compare:
                # 新结点小于父结点
                parent.nodes.insert(0, tree_node.nodes[0])
                parent.child_list[0] = tree_node.child_list[1]
                parent.child_list[0].parent = parent
                parent.child_list.insert(0, tree_node.child_list[0])
                parent.child_list[0].parent = parent
                parent.child_list.pop()
            else:
                # 新结点大于父结点第一个元素 小于第二个元素
                parent.nodes.insert(1, tree_node.nodes[0])
                parent.child_list[1] = tree_node.child_list[1]
                parent.child_list[1].parent = parent
                parent.child_list.insert(1, tree_node.child_list[0])
                parent.child_list[2].parent = parent
                parent.child_list.pop()
            return parent
        else:
            return tree_node

    def __str__(self) -> str:
        return str(self.root)

    def push_arr(self):
        return self.root.push_arr()


class DrawTree(tkinter.Tk):

    def __init__(self, class_name, width, height, tree: TwoThreeTree):
        # offset = 5
        self.width = width
        self.height = height
        # x2 = width + offset
        # y2 = height + offset
        super().__init__(className=class_name)
        self.geometry('%dx%d' % (self.width, self.height))
        self.canvas = tkinter.Canvas(self, width=width, height=height)
        self.canvas.pack()
        self.draw(self.canvas, tree)

    def draw(self, canvas, ttTree: TwoThreeTree):
        # 将树的结点存为数组
        arr = ttTree.push_arr()
        offset = 15
        node_height = 90
        node_width = 30
        mid = self.width / 2
        font = ('Couried', 14)
        for tree_node in arr:
            node_text = ''
            for node in tree_node.nodes:
                node_text += str(node.data) + ' '
            if tree_node.parent is None or not hasattr(tree_node.parent, 'x'):
                # 根结点
                # canvas.create_oval(mid - node_width / 2, offset, mid + node_width / 2, offset + node_height,
                #                    fill='lightblue')
                tree_node.x, tree_node.y = mid - node_width / 2, offset
                canvas.create_text(tree_node.x, tree_node.y, text=node_text, font=font)
            else:
                # 求当前层节点数,第i层的结点总数不超过 Math.pow(2,i)
                max_nodes = math.pow(2, tree_node.tree_level - 2)
                # 根据当前层节点数计算x坐标每个节点的位移量
                x_distance = int(self.width // max_nodes - offset) >> 2
                # 根据父节点计算坐标
                parent_x, parent_y = tree_node.parent.x, tree_node.parent.y
                if tree_node.sub_type == 0:
                    # 左结点
                    tree_node.x, tree_node.y = parent_x - x_distance + offset*2, parent_y + node_height
                elif tree_node.sub_type == 2:
                    # 右结点
                    tree_node.x, tree_node.y = parent_x + x_distance - offset*2, parent_y + node_height
                else:
                    # 中结点
                    tree_node.x, tree_node.y = parent_x, parent_y + node_height
                canvas.create_line(parent_x, parent_y, tree_node.x, tree_node.y, fill='red')
                canvas.create_text(tree_node.x, tree_node.y, text=node_text, font=font)
        self.mainloop()


if __name__ == '__main__':
    tree = TwoThreeTree()
    # for i in [10, 1, 6, 0, 9, 7, 0, 8, 9, 8]:
    for i in range(20):
        # tree.add_node(Node(i))
        # DrawTree('tree', 800, 600, tree)
        # tree.add_node(Node(i))
        randint = random.randint(0, 15)
        print(randint)
        tree.add_node(Node(randint))
    print(tree)
    DrawTree('tree', 800, 600, tree)
    # for item in tree.push_arr():
    #     print('subType', item['subType'])
    #     for node in item['nodes']:
    #         print(node.data, end=',')
    #     print()
