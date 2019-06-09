import random
import tkinter

import math


class Node:

    def __init__(self, data) -> None:
        self.data = data
        # 初始化节点层数
        self.level = 1
        self.left = None
        self.right = None
        self.count = 1

    def compare(self, other) -> int:
        # 定义节点对比方法
        if self.data > other.data:
            return 1
        elif self.data < other.data:
            return -1
        return 0

    def add_count(self, num):
        self.count += num
        return self

    def __str__(self) -> str:
        # 中序遍历
        concat_str = ''
        if self.left is not None:
            concat_str += str(self.left)
        concat_str += ('data:%d--\tcount:%d--\tlevel:%d\n' % (
            self.data, self.count, self.level))
        if self.right is not None:
            concat_str += str(self.right)
        return concat_str

    def inorder_traversal(self, parent_data=None):
        # 前序遍历
        concat_str = ('data:%d--\tparent_data:%s---\tcount:%d--\tlevel:%d\n' % (
            self.data, parent_data, self.count, self.level))
        if self.left is not None:
            concat_str += self.left.inorder_traversal(self.data)
        if self.right is not None:
            concat_str += self.right.inorder_traversal(self.data)
        return concat_str

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


class AvlTree:

    def __init__(self) -> None:
        self.root = None
        self.size = 0

    # 获取平衡因子
    def get_balance_factor(self, node: Node):
        return self.get_height(node.left) - self.get_height(node.right)

    # 是否平衡二叉树
    def is_avl(self):
        stack = [self.root]
        while len(stack) > 0:
            pop = stack.pop()
            if abs(self.get_balance_factor(pop)) > 1:
                return False
        return True

    @staticmethod
    def get_height(node: Node):
        return 0 if node is None else node.level

    def add_node(self, node: Node):
        self.size += 1
        if self.root is None:
            self.root = node
        else:
            self.root = self.__add_node(self.root, node)

    # 添加后返回当前子树的根结点
    def __add_node(self, curr: Node, node: Node) -> Node:
        if curr is None:
            return node
        else:
            compare = curr.compare(node)
            if compare == 1:
                curr.left = self.__add_node(curr.left, node)
            elif compare == -1:
                curr.right = self.__add_node(curr.right, node)
            else:
                curr = curr.add_count(1)
            # 计算层级
            curr = self.recount_level(curr)
            return curr

    def remove_data(self, data):
        self.root = self.remove_node(data, self.root)

    def remove_node(self, data, node):
        if node is None:
            return None
        result_node = node
        if data < node.data:
            node.left = self.remove_node(data, node.left)
            # node = self.recount_level(node)
        elif data > node.data:
            node.right = self.remove_node(data, node.right)
            # node = self.recount_level(node)
        if data == node.data:
            # 删除节点
            if node.left is None:
                # 左结点为空时,用右结点替换被删除的结点
                result_node = node.right
            elif node.right is None:
                result_node = node.left
            else:
                # 左右均有结点,获取右子树中的最小值->替换被删除的结点
                min_node = self.get_min(node.right)
                min_node.right = self.remove_node(min_node.data, node.right)
                # 将替换的元素扣减的长度加回来
                self.size += min_node.count
                min_node.left = node.left
                result_node = min_node
            self.size -= node.count
        # 重算高度
        if result_node is not None:
            result_node = self.recount_level(result_node)
        return result_node

    # 添加/删除元素后将树整理为平衡二叉树
    def recount_level(self, result_node):
        result_node.level = max(self.get_height(result_node.left), self.get_height(result_node.right)) + 1
        balance_factor = self.get_balance_factor(result_node)
        if abs(balance_factor) > 1:
            # RR LL时 符号必须为大于或等于，否则当左/右子树高且子结点平衡时无法继续整理
            if balance_factor > 1 and self.get_balance_factor(result_node.left) >= 0:
                # 左子树高,且左节点的左子树大于等于右子树,进行右旋 RR
                result_node = self.right_rotate(result_node)
            elif balance_factor < -1 and self.get_balance_factor(result_node.right) <= 0:
                # 右子树高,且右节点的右子树大于等于左子树高,进行左旋 LL
                result_node = self.left_rotate(result_node)
            elif balance_factor > 1 and self.get_balance_factor(result_node.left) < 0:
                # 左子树高,且左节点的右子树高,左节点先左旋父结点再右旋 LR
                result_node.left = self.left_rotate(result_node.left)
                result_node = self.right_rotate(result_node)
            elif balance_factor < -1 and self.get_balance_factor(result_node.right) > 0:
                # 右子树高,且右节点的左子树高,右节点先右旋父结点再左旋 RL
                result_node.right = self.right_rotate(result_node.right)
                result_node = self.left_rotate(result_node)
        return result_node

    # 获取子树中的最小结点
    def get_min(self, node):
        if node.left is None:
            # 当不存在左结点时 即为最小值
            return node
        return self.get_min(node.left)

    # 查找结点
    def find_data(self, data):
        return self.find_node(data, self.root)

    def find_node(self, data, node: Node):
        if node is None:
            return None
        if data == node.data:
            return node
        elif data < node.data:
            return self.find_node(data, node.left)
        elif data > node.data:
            return self.find_node(data, node.right)

    def __str__(self) -> str:
        return 'size:%s\n%s' % (self.size, str(self.root))

    def inorder_traversal(self):
        # 中序遍历
        return self.root.inorder_traversal()

    # 右旋
    # 对节点y进行向右旋转操作，返回旋转后新的根节点x
    #        y                              x
    #       / \                           /   \
    #      x   T4     向右旋转 (y)        z     y
    #     / \       - - - - - - - ->    / \   / \
    #    z   T3                       T1  T2 T3 T4
    #   / \
    # T1   T2
    @staticmethod
    def right_rotate(y) -> Node:
        x = y.left
        y.left, x.right = x.right, y
        AvlTree.flush_level(y)
        AvlTree.flush_level(x)
        return x

    # 左旋
    # 对节点y进行向左旋转操作，返回旋转后新的根节点x
    #    y                             x
    #  /  \                          /   \
    # T1   x      向左旋转 (y)       y     z
    #     / \   - - - - - - - ->   / \   / \
    #   T2  z                     T1 T2 T3 T4
    #      / \
    #     T3 T4
    @staticmethod
    def left_rotate(y) -> Node:
        x = y.right
        y.right, x.left = x.left, y
        # 重算层级
        AvlTree.flush_level(y)
        AvlTree.flush_level(x)
        return x

    @staticmethod
    def flush_level(node):
        node.level = max(AvlTree.get_height(node.left), AvlTree.get_height(node.right)) + 1

    def push_arr(self):
        return self.root.push_arr()


class DrawTree(tkinter.Tk):

    def __init__(self, class_name, width, height, tree: AvlTree):
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

    def draw(self, canvas, avl_tree: AvlTree):
        # 将树的结点存为数组
        arr = avl_tree.push_arr()
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
                canvas.create_text(node.x, node.y, text=node.data, font=font)

        self.mainloop()


if __name__ == '__main__':
    tree = AvlTree()
    temp = []
    for i in range(30):
        randint = random.randint(0, 50)
        temp.append(randint)
        tree.add_node(Node(randint))
    print(temp)
    # for i in [27, 7, 23, 36, 45, 40, 23, 12, 18, 6, 44, 22, 13, 21, 21, 6, 0, 20, 37, 11, 15, 6, 47, 32, 25, 14, 17, 32, 10, 12]:
    #     tree.add_node(Node(i))
    print(tree)
    print(tree.inorder_traversal())
    print(tree.is_avl())
    # 根据树的层级计算宽度/间隔->画出树
    DrawTree('avlTree', 800, 600, tree)
    # 删除10-15
    for i in range(10, 16, 1):
        if tree.find_data(i) is not None:
            tree.remove_data(i)
            # DrawTree('avlTree', 800, 600, tree)
    print(tree)
    print(tree.is_avl())
    DrawTree('avlTree', 800, 600, tree)
    # [31, 14, 42, 50, 30, 36, 7, 30, 38, 25, 46, 8, 2, 7, 45, 34, 31, 15, 3, 7, 7, 18, 11, 27, 5, 6, 24, 32, 46, 31]
