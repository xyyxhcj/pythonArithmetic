import random


class Node:

    def __init__(self, data) -> None:
        self.data = data
        # 初始化节点层数，平衡因子
        self.level = 1
        self.balanceFactor = 0
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
        concat_str += ('%d--%d\n' % (self.data, self.count))
        if self.right is not None:
            concat_str += str(self.right)
        return concat_str


class AvlTree:

    def __init__(self) -> None:
        self.root = None
        self.add_lambda = {
            # 改为对left/right 赋值
            1: lambda  curr, node: self.__add_node(curr.left, node),
            -1: lambda curr, node: self.__add_node(curr.right, node),
            0: lambda curr, node: curr.add_count(1)
        }

    def add_node(self, node: Node):
        if self.root is None:
            self.root = node
        else:
            self.__add_node(self.root, node)

    # 添加后返回当前子树的根结点
    def __add_node(self, curr: Node, node: Node) -> Node:
        if curr is None:
            return node
        else:
            compare = curr.compare(node)
            if compare == 1:
                curr.left = self.add_lambda[compare](curr, node)
            elif compare == -1:
                curr.right = self.add_lambda[compare](curr, node)
            else:
                self.add_lambda[compare](curr, node)
            return curr

    def __str__(self) -> str:
        return str(self.root)


if __name__ == '__main__':
    tree = AvlTree()
    for i in range(10):
        tree.add_node(Node(random.randint(0, 15)))

    print(tree)
