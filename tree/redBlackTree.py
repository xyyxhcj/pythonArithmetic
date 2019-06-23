# 红黑树
import random
import tkinter

import math

BLACK = True
RED = False


class Node:
    def __init__(self, data):
        self.data = data
        self.color = RED
        self.count = 1
        self.left = None
        self.right = None

    def compare(self, other) -> int:
        if self.data < other.data:
            return -1
        elif self.data > other.data:
            return 1
        else:
            return 0

    def __str__(self) -> str:
        return '%d:%d' % (self.data, self.count)

        # 以前序遍历的方式将节点放入list

    def push_arr(self, parent=None, sub_type=None, tree_level=1) -> list:
        self.parent = parent
        self.sub_type = sub_type
        self.tree_level = tree_level
        arr = [self]
        if self.left is not None:
            arr += self.left.push_arr(self, 'L', tree_level + 1)
        if self.right is not None:
            arr += self.right.push_arr(self, 'R', tree_level + 1)
        return arr


# 左倾红黑树
class RbTree:
    def __init__(self) -> None:
        self.root = None
        self.size = 0

    def add_node(self, node: Node):
        self.size += 1
        if self.root is None:
            self.root = node
        else:
            self.root = self.__add_node(self.root, node)
        self.root.color = BLACK

    # 添加2R
    #       /             /           /            /
    #      3B            3B          2B          2R
    #     /  \   ->     / \     ->  /  \   ->   /  \
    #    1R   T2       2R  T2     1R   3R     1B  3B
    #   / \           /  \            /  \       /  \
    #  T3  2R        1R   T1         T1  T2     T1  T2
    #     / \       /  \
    #    T4 T1     T3  T4
    def __add_node(self, root, node):
        if root is None:
            return node
        compare = root.compare(node)
        if compare == 1:
            # 新结点小
            root.left = self.__add_node(root.left, node)
        elif compare == -1:
            # 新结点大
            root.right = self.__add_node(root.right, node)
        else:
            root.count += 1
            return root
        if root.right is not None and root.right.color == RED and (root.left is None or root.left.color != RED):
            root = self.left_rotate(root)
        if root.left is not None:
            if root.left.left is not None and root.left.color == RED and root.left.left.color == RED:
                root = self.right_rotate(root)
            if root.right is not None and root.right.color == RED and root.left.color == RED:
                root = self.flip_colors(root)
        return root

    # 颜色翻转
    #    /            /
    #   2B          2R
    #  /  \   ->   /  \
    # 1R   3R     1B  3B
    @staticmethod
    def flip_colors(node):
        node.color = RED
        node.left.color = node.right.color = BLACK
        return node

    # 右旋转
    #        /           /
    #       3B          2B
    #      / \     ->  /  \
    #     2R  T2     1R   3R
    #    /  \            /  \
    #   1R   T1         T1  T2
    @staticmethod
    def right_rotate(node):
        root = node.left
        node.left = root.right
        root.right = node
        root.color = BLACK
        node.color = RED
        return root

    # 左旋转
    #     /             /
    #    1R/B   ->     2R/B
    #   / \           /
    #  T3  2R        1R
    #     /         /  \
    #    T4        T3  T4
    @staticmethod
    def left_rotate(node):
        root = node.right
        node.right = root.left
        root.left = node
        # 交换颜色,使根结点颜色与插入前一致
        root.color, node.color = node.color, root.color
        return root

    def push_arr(self):
        return self.root.push_arr()


class DrawTree(tkinter.Tk):

    def __init__(self, class_name, width, height, tree: RbTree):
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

    def draw(self, canvas, rb_tree: RbTree):
        # 将树的结点存为数组
        arr = rb_tree.push_arr()
        offset = 10
        node_height = 90
        node_width = 30
        mid = self.width / 2
        font = ('Couried', 15)
        for node in arr:
            if node.parent is None:
                # 根结点
                # canvas.create_oval(mid - node_width / 2, offset, mid + node_width / 2, offset + node_height,
                #                    fill='lightblue')
                node.x, node.y = mid - node_width / 2, offset
                canvas.create_text(node.x, node.y, text=node.data, font=font)
            else:
                # 求当前层节点数,第i层的结点总数不超过 Math.pow(2,i)
                max_nodes = math.pow(2, node.tree_level - 2)
                # 根据当前层节点数计算x坐标每个节点的位移量
                x_distance = int(self.width // max_nodes - offset) >> 2
                # 根据父节点计算坐标
                parent_x, parent_y = node.parent.x, node.parent.y
                if node.sub_type == 'L':
                    # 左结点
                    node.x, node.y = parent_x - x_distance, parent_y + node_height
                else:
                    # 右结点
                    node.x, node.y = parent_x + x_distance, parent_y + node_height
                canvas.create_line(parent_x, parent_y, node.x, node.y, fill='red')
                if node.color == RED:
                    canvas.create_text(node.x, node.y, text=node.data, font=font, fill='red')
                else:
                    canvas.create_text(node.x, node.y, text=node.data, font=font)

        self.mainloop()


if __name__ == '__main__':
    tree = RbTree()
    temp = []
    for i in range(15):
        randint = random.randint(0, 50)
        temp.append(randint)
        tree.add_node(Node(randint))
        # tree.add_node(Node(i))
        # DrawTree('rbTree', 800, 600, tree)
    print(temp)
    # for i in [27, 7, 23, 36, 45, 40, 23, 12, 18, 6, 44, 22, 13, 21, 21, 6, 0, 20, 37, 11, 15, 6, 47, 32, 25, 14, 17, 32, 10, 12]:
    #     tree.add_node(Node(i))
    # 根据树的层级计算宽度/间隔->画出树
    DrawTree('rbTree', 800, 600, tree)
