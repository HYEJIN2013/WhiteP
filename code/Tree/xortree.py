# 429A
# Xor-tree

class Node:
    def __init__(self, name, value, parent = None):
        self.name = 0
        self.value = 0
        self.grandChildren = list()
        self.setParent(parent)

    def setParent(self, parent):
        self.parent = parent
        if parent is not None:
            self.grandParent = parent.parent
            self.depth = parent.depth + 1
            if self.grandParent is not None:
                self.grandParent.grandChildren.append(self)
        else:
            self.grandParent = None
            self.depth = 0

def xorRecursive(node):
    node.value = node.value ^ 1
    for grandChild in node.grandChildren:
        xorRecursive(grandChild)

count = int(raw_input())
nodes = dict()
for i in range(count):
    nodes[i + 1] = Node(i + 1, 0)

for i in range(count - 1):
    temp = [int(val) for val in raw_input().split()]
    nodes[temp[0]].setParent(nodes[temp[1]])

temp = [int(val) for val in raw_input().split()]
for i in range(count):
    nodes[i + 1].value = temp[i]

goals = [int(val) for val in raw_input().split()]
steps = list()
for i in range(count):
    if nodes[i + 1].value != goals[i]:
        steps.append(str(i + 1))
        xorRecursive(nodes[i + 1])
print(len(steps))
print('\n'.join(steps))
