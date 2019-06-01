class Node:
    def __init__(self, parent_node=None, value=0):
        self.parent_node = parent_node
        self.value = value
        self.sum = value
        self.next = dict()


class MapSum:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = Node()

    def insert(self, key: str, val: int) -> None:
        node = self.root
        for c in key:
            if c not in node.next:
                node.next[c] = Node(node)
            node = node.next[c]
        self.update_value(node, val)

    def sum(self, prefix: str) -> int:
        node = self.root
        for c in prefix:
            if c not in node.next:
                return 0
            node = node.next[c]
        return node.sum

    @staticmethod
    def update_value(node, val):
        temp = val - node.value
        if temp != 0:
            node.value = val
            while node is not None:
                node.sum += temp
                node = node.parent_node


if __name__ == '__main__':
    map_sum = MapSum()
    map_sum.insert("apple", 3)
    print(map_sum.sum("ap"))
    map_sum.insert("app", 2)
    print(map_sum.sum("ap"))
