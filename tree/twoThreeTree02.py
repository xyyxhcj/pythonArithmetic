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
            # 层数
            self.level = 1
            # 子结点数量
            self.count = 1
        else:
            self.level = 0
            self.count = 0
        self.child_list = [None] * 4

    # 校验子树是否平衡
    def is_balance(self):
        curr_level = None
        is_balance = True
        for child in self.child_list:
            if child is not None:
                if curr_level is None:
                    curr_level = child.level
                elif curr_level != child.level:
                    is_balance = False
                    break
        return is_balance
    # todo
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
        # 存储子树高度,删除时如果高度变更则触发父结点整理 todo
        self.height = 1

    def add_node(self, node: Node):
        self.size += 1
        if self.root is None:
            self.root = TreeNode(node)
        else:
            self.root = self.__add_node(self.root, node)

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

    # 删除结点
    def remove_node(self, node: Node):
        self.root = self.__remove_node(self.root, node)

    # 如果待删除元素存在且为非叶子节点,用后继的叶子节点的值替代要删除的节点元素,将删除问题转移到叶子节点,避免子分支的处理
    def __remove_node(self, tree_node: TreeNode, node: Node, parent: TreeNode = None) -> TreeNode:
        if tree_node is None:
            return parent
        tree_node_compare = tree_node.compare(node)
        if CONSTANT['GREATER'] == tree_node_compare:
            # 新结点小
            tree_node = self.__remove_node(tree_node.child_list[0], node, tree_node)
        elif CONSTANT['MIDDLE'] == tree_node_compare:
            tree_node = self.__remove_node(tree_node.child_list[1], node, tree_node)
        elif CONSTANT['LESS'] == tree_node_compare:
            # 新结点大
            if len(tree_node.nodes) > 1:
                tree_node = self.__remove_node(tree_node.child_list[2], node, tree_node)
            else:
                tree_node = self.__remove_node(tree_node.child_list[1], node, tree_node)
        elif CONSTANT['LEFT'] == tree_node_compare:
            # 删除左结点
            self.size -= tree_node.nodes[0].count
            if tree_node.child_list[1] is None:
                remove_node = tree_node
            else:
                # 获取右/中子树的最小树节点，替换，再删除移至叶子节点的原节点
                remove_node = self.get_min(tree_node.child_list[1])
                # 交换,treeNode中的最小结点索引必为0
                self.swap(tree_node.nodes[0], remove_node.nodes[0])
            # 删除treeNode下的第一个结点
            self.delete_node(remove_node)
        else:
            # 删除右结点
            self.size -= tree_node.nodes[1].count
            if tree_node.child_list[1] is None:
                # 当前已经为叶子节点
                tree_node.nodes[1].pop()
            else:
                # 获取右子树的最小树节点(treeNode中的最小结点索引必为0)，替换，再删除移至叶子节点的原节点
                remove_node = self.get_min(tree_node.child_list[1])
                # 交换,treeNode中的最小结点索引必为0
                self.swap(tree_node.nodes[1], remove_node.nodes[0])
                # 删除treeNode下的第一个结点
                self.delete_node(remove_node)
        if parent is None:
            return tree_node
        else:
            return tree_node.parent

    # 获取当前treeNode子树中最小的node(返回该node所在的TreeNode及该node在nodes中的索引)
    def get_min(self, tree_node) -> TreeNode:
        if tree_node.child_list[0] is None:
            return tree_node
        else:
            return self.get_min(tree_node.child_list[0])

    # 交换结点数据
    @staticmethod
    def swap(node1, node2):
        node1.count, node2.count = node2.count, node1.count
        node1.data, node2.data = node2.data, node1.data

    # 删除treeNode下的第一个结点,当前为叶子节点
    # 删除3
    #     5,8               5,8
    #   /  |  \      ->   /  |  \
    # 3,4 6,7 9,10       4  6,7 9,10

    #     5,8               6,8
    #   /  |  \      ->   /  |  \
    #  3  6,7 9,10       5   7  9,10

    #     5               9
    #    / \      ->     / \
    #   3   9,10        5  10

    #     5,8                8
    #   /  |  \      ->     / \
    #  3   6  9,10       5,6   9,10

    #    5    ->    5,9
    #   / \
    #  3   9
    @staticmethod
    def delete_node(remove_node: TreeNode):
        # 如果树结点存在双结点,则直接将第二个结点替换当前结点
        if len(remove_node.nodes) > 1:
            remove_node.nodes[0] = remove_node.nodes.pop()
        else:
            tree_parent = remove_node.parent
            if len(tree_parent.child_list[1].nodes) > 1:
                # 中/右子结点为双结点
                tree_parent.child_list[0] = TreeNode(tree_parent.nodes[0], tree_parent)
                tree_parent.nodes[0] = tree_parent.child_list[1].nodes[0]
                tree_parent.child_list[1].nodes[0] = tree_parent.child_list[1].nodes.pop()
            else:
                # 中间/右子结点为单结点
                if len(tree_parent.nodes) > 1:
                    # 父结点为双元素
                    tree_parent.child_list[0] = TreeNode(tree_parent.nodes[0], tree_parent)
                    tree_parent.child_list[0].nodes.append(tree_parent.child_list[1].nodes[0])
                    tree_parent.nodes[0] = tree_parent.nodes.pop()
                    tree_parent.child_list[1], tree_parent.child_list[2] = tree_parent.child_list[2], None
                else:
                    # 父结点为单元素 todo 无法维持树的平衡,需要向上触发父结点进行整理
                    # 计算到第几层可实现平衡,
                    tree_parent.nodes.append(tree_parent.child_list[1].nodes[0])
                    tree_parent.child_list[0] = tree_parent.child_list[1] = None


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
            for i in range(len(tree_node.nodes)):
                node_text += str(tree_node.nodes[i].data)
                if i != len(tree_node.nodes) - 1:
                    node_text += ','
            # for node in tree_node.nodes:
            #     node_text += str(node.data) + ','
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
                    tree_node.x, tree_node.y = parent_x - x_distance + offset * 2, parent_y + node_height
                elif tree_node.sub_type == 2:
                    # 右结点
                    tree_node.x, tree_node.y = parent_x + x_distance - offset * 2, parent_y + node_height
                else:
                    # 中结点
                    tree_node.x, tree_node.y = parent_x, parent_y + node_height
                canvas.create_line(parent_x, parent_y, tree_node.x, tree_node.y, fill='red')
                canvas.create_text(tree_node.x, tree_node.y, text=node_text, font=font)
        self.mainloop()


if __name__ == '__main__':
    tree = TwoThreeTree()
    # for i in [3, 11, 6, 12, 2, 10, 15, 7, 8, 0, 4, 9]:
    for i in range(20):
        # tree.add_node(Node(i))
        # DrawTree('tree', 800, 600, tree)
        # tree.add_node(Node(i))
        randint = random.randint(0, 50)
        # randint = i
        print('add %d' % randint)
        tree.add_node(Node(randint))
    print(tree)
    DrawTree('tree', 800, 600, tree)
    # for i in range(5):
    #     print('remove %d' % i)
    #     tree.remove_node(Node(i))
    #     DrawTree('tree', 800, 600, tree)

# todo 准备重构 重写一个py 在每个节点存储子结点数量及层数，平衡因子
#       提取减少结点数量方法，向父结点不断递归，减少后判断平衡因子，不为0时则判断总结点数量是否无法满足当前层数的最小数量,不满足则不断向父级递归，直至根结点，如果仍不满足，则缩小整棵树的层级
