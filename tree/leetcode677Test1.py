class Node:
    def __init__(self, value=0):
        self.value = value
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
                node.next[c] = Node()
            node = node.next[c]
        node.value = val

    def sum(self, prefix: str) -> int:
        node = self.root
        for c in prefix:
            if c not in node.next:
                return 0
            node = node.next[c]
        sum = 0
        stack = [node]
        while len(stack) > 0:
            pop = stack.pop()
            sum += pop.value
            for n in pop.next.values():
                stack.append(n)
        return sum
