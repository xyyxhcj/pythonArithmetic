from collections import deque


class Node:
    def __init__(self, is_word=False):
        self.is_word = is_word
        self.next = dict()


class WordDictionary:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = Node()

    def addWord(self, word: str) -> None:
        """
        Adds a word into the data structure.
        """
        node = self.root
        for c in word:
            if c not in node.next:
                node.next[c] = Node()
            node = node.next[c]
        if node.is_word is False:
            node.is_word = True

    def search(self, word: str) -> bool:
        """
        Returns if the word is in the data structure. A word could contain the dot character '.' to represent any one letter.
        """
        queue = deque([{'node': self.root, 'index': 0}])
        length = len(word)
        while len(queue) > 0:
            pop = queue.popleft()
            node = pop['node']
            index = pop['index']
            if index == length:
                if node.is_word:
                    return True
                else:
                    continue
            c = word[index]
            if c == '.':
                for n in node.next.values():
                    queue.append({'node': n, 'index': index + 1})
            else:
                if c in node.next:
                    queue.append({'node': node.next[c], 'index': index + 1})
        return False

# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)
