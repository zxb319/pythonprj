class BinTree:
    def __init__(self):
        self._root = None

    class _Node:
        def __init__(self, val, left: 'BinTree._Node' = None, right: 'BinTree._Node' = None):
            self.val = val
            self.left = left
            self.right = right

    def _insert(self, root: '_Node', node: '_Node'):
        if not root:
            return node
        elif node.val < root.val:
            root.left = self._insert(root.left, node)
        else:
            root.right = self._insert(root.right, node)
        return root

    def insert(self, val):
        new_node = self._Node(val)
        self._root = self._insert(self._root, new_node)

    def _search(self, root: '_Node', val):
        if not root:
            return None
        elif val < root.val:
            return self._search(root.left, val)
        elif root.val < val:
            return self._search(root.right, val)
        else:
            return root

    def search(self, val):
        res = self._search(self._root, val)
        if not res:
            return None
        else:
            return res.val

    def __str__(self):
        res = []

        def inner(root: 'BinTree._Node'):
            if root:
                yield root
                yield from inner(root.left)
                yield from inner(root.right)

        for node in inner(self._root):
            if node.left:
                res.append(str(node.val)+'.left->'+str(node.left.val))
            if node.right:
                res.append(str(node.val)+'.right->'+str(node.right.val))

        return '\n'.join(res)


if __name__ == '__main__':
    t = BinTree()
    t.insert(3)
    t.insert(1)
    t.insert(4)
    t.insert(5)
    t.insert(9)
    t.insert(2)

    print(t)


