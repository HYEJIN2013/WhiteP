class Node:
  def __init__(self, value):
    self.value = value
    self.children = []
    self.complete = False


elemset = set()  # let's assume this is filled with the elements (lowercased)
word = ''  # let's assume this is the word
root = Node(None)

def build_tree(node, word):
  if not word:
    node.complete = True
    return
  
  if word[0].lower() in elemset:
    child = Node(word[0])
    node.children.append(child)
    build_tree(child, word[1:])
  if len(word) > 1 and word[:2].lower() in elemset:
    child = Node(word[:2])
    node.children.append(child)
    build_tree(child, word[2:])

build_tree(root, word)

# now your tree should contain all the words
# nodes marked complete should represent finsihed words
