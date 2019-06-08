import random
import tkinter


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
    def push_arr(self, parent=None) -> list:
        self.parent = parent
        arr = [self]
        if self.left is not None:
            arr += self.left.push_arr(self)
        if self.right is not None:
            arr += self.right.push_arr(self)
        return arr


class AvlTree:

    def __init__(self) -> None:
        self.root = None

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
            curr.level = max(self.get_height(curr.left), self.get_height(curr.right)) + 1
            # 平衡因子绝对值大于1时,进行左旋/右旋
            if abs(self.get_balance_factor(curr)) > 1:
                if self.get_balance_factor(curr) > 1 and self.get_balance_factor(curr.left) > 0:
                    # 左子树高,且左节点的左子树高,进行右旋 RR
                    curr = self.right_rotate(curr)
                elif self.get_balance_factor(curr) < 1 and self.get_balance_factor(curr.right) < 0:
                    # 右子树高,且右节点的右子树高,进行左旋 LL
                    curr = self.left_rotate(curr)
                elif self.get_balance_factor(curr) > 1 and self.get_balance_factor(curr.left) < 0:
                    # 左子树高,且左节点的右子树高,左节点先左旋父结点再右旋 LR
                    curr.left = self.left_rotate(curr.left)
                    curr = self.right_rotate(curr)
                elif self.get_balance_factor(curr) < 1 and self.get_balance_factor(curr.right) > 0:
                    # 右子树高,且右节点的左子树高,右节点先右旋父结点再左旋 RL
                    curr.right = self.right_rotate(curr.right)
                    curr = self.left_rotate(curr)
            return curr

    def __str__(self) -> str:
        return str(self.root)

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
        offset = 5
        node_height = 30
        node_width = 30
        mid = self.width / 2
        # 根结点
        root = avl_tree.root
        canvas.create_oval(mid - node_width / 2, offset, mid + node_width / 2, offset + node_height, fill='lightblue')
        tkinter.Label(canvas, text=root.data).pack()

        # 通过父节点动态计算坐标,并连线
        self.mainloop()
        # if step < 3:
        #     step = 3
        # if start_x > end_x or start_y > end_y:
        #     self.mainloop()
        #     return
        # if depth % 2 == 0:
        #     canvas.create_oval(start_x, start_y, end_x, end_y, fill='lightblue', width=2)
        # else:
        #     canvas.create_oval(start_x, start_y, end_x, end_y, fill='Violet', width=2)
        # self.draw(canvas, start_x + step, start_y + step, end_x - step, end_y - step, step, depth + 1)


if __name__ == '__main__':
    tree = AvlTree()
    for i in range(10):
        tree.add_node(Node(random.randint(0, 15)))
    # for i in [1, 6, 12, 12, 3, 9, 4, 12, 7, 6]:
    #     tree.add_node(Node(i))
    print(tree)
    print(tree.inorder_traversal())
    print(tree.is_avl())
    DrawTree('avlTree', 800, 600, tree)
    # TODO 根据树的层级计算宽度/间隔->构造树形图
