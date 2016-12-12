class Node:
    def __init__(self, value, left, right):
        (self.value, self.left, self.right) = (value, left, right)

    def preorder(tree):
        if tree.value:
            print tree.value
        if tree.left:
            Node.preorder(tree.left)
        if tree.right:
            Node.preorder(tree.right)

    def inorder(tree):
        if tree.left:
            Node.inorder(tree.left)
        if tree.value:
            print tree.value
        if tree.right:
            Node.inorder(tree.right)

    def postorder(tree):
        if tree.left:
            Node.postorder(tree.left)
        if tree.right:
            Node.postorder(tree.right)
        if tree.value:
            print tree.value

if __name__ == '__main__':
    left  = Node(2, Node('asdf', None, None), Node(11, None, None))
    right = Node(7, None, Node(15, Node(65, None, None), None))
    tree  = Node(4, left, right)

    print('Preorder')
    Node.preorder(tree)
    print('Inorder')
    Node.inorder(tree)
    print('Postorder')
    Node.postorder(tree)
