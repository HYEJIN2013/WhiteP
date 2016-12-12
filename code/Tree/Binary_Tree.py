class Node:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.data = val

    def insert(self, node):
        if self.data < node.data:
            if self.left is None:
                self.left = node
            else:
                self.left.insert(node)
        if self.data > node.data:
            if self.right is None:
                self.right = node
            else:
                self.right.insert(node)

    def printTree(self):
        print self.data,
        if self.left:
            self.left.printTree()
        if self.right:
            self.right.printTree()

    def compareTree(self, node):
        if node is None:
            return False
        if self.data != node.data:
            return False
        res = True

        if self.left is None:
            if node.left:
                return False
        else:
            res = self.left.compareTree(node.left)

        if res is False:
            return False

        if self.right is None:
            if node.right:
                return False
        else:
            res = self.right.compareTree(node.right)

        return res

def binary_equal(t1, t2):
    if t1 == t2:
        return True
    if t1 == None or t2 == None:
        return False
    return t1.data==t2.data and binary_equal(t1.left, t2.left) and binary_equal(t1.right, t2.right)


def buildTree(inputs):
    if not inputs:
        return None
    root = Node(inputs[0])
    for i in inputs[1:]:
        root.insert(Node(i))
    root.printTree()
    print
    return root
