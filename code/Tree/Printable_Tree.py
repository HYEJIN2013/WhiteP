import math
from collections import deque

class Node:
  balanceFactor = 0
  height = 0
  lchild = None
  rchild = None
  def __init__(self, key):
    self.key = key 

class Tree:
  root = None
  def __init__(self):
    pass 
  
  def insert(self, n):
    """ Insert a node into the tree """
    if not self.root:
      self.root = n

  @staticmethod
  def height(tree):
    """ Conduct a depth first search to confirm max height of tree"""
    return Tree._depthTraverseCalculateHeight(tree,0)

  @staticmethod
  def _depthTraverseCalculateHeight(node, height):
    lheight = 0
    rheight = 0
    height = height+1

    if(node.lchild):
      lheight = Tree._depthTraverseCalculateHeight(node.lchild,height) 

    if(node.rchild):
      rheight = Tree._depthTraverseCalculateHeight(node.rchild,height)

    if(not node.lchild and not node.rchild):
      return height

    return max(lheight, rheight)

  @property
  def width_with_empty_leaves(self):
    return int(math.pow(2,Tree.height(self.root)-1))

  @property
  def width(self):
    """ Conduct a breadth first search to confirm max width of tree"""
    level = 1 
    width = 0
    cq = deque([])
    nq = deque([])

    #Enqueue root
    if width == 0:
      cq.append(self.root)
      level += 1
      width = 1

    while(cq):
      cur = cq.popleft()
      
      if(cur.lchild):
        nq.append(cur.lchild)
      if(cur.rchild):
        nq.append(cur.rchild)
      
      if(not cq and nq):
        if(len(nq) > width):
          width = len(nq)
        cq = nq
        nq = deque([])
        level += 1

    return width 

  @staticmethod
  def get_key_line(height, level, keys, spacing, spacing_char=' '):
    result = ""
    num_keys = None
    line_width = (spacing * int(math.pow(2,(height-1)))) - (spacing * 2) 

    num_keys = int(math.pow(2,(level-1)))
    space_per_key = int(math.ceil(line_width * 1.0  / num_keys))
    
    for i in range(len(keys)):
      key_string = str(keys[i])
      spacing = (space_per_key - len(key_string))/2

      pre_spacing = spacing

      if (space_per_key - len(key_string)) % 2 != 0:
        pres_pacing = spacing + 1

      if(space_per_key % 2 != 0 and len(key_string) % 2 == 0):
        column = pre_spacing * spacing_char + key_string + spacing * spacing_char + spacing_char
      elif(space_per_key % 2 == 0 and len(key_string) % 2 != 0):
        column = pre_spacing * spacing_char + key_string + spacing * spacing_char + spacing_char
      else:
        column = pre_spacing * spacing_char + key_string + spacing * spacing_char

      result = result + column

    return result

  def print_tree(self):
    """ Conduct a breadth first traversal to print tree"""
    print 30 * "="
    print "Tree [height: {0}, width: {1}]".format(self.height, self.width_with_empty_leaves)
    print ""
    
    spacing = 5  

    level = 1 
    item = 0
    non_none_flag = True
    cq = deque([])
    nq = deque([])
    current_level_key_list = ["NONE"]

    #Enqueue root
    if level == 1:
      cq.append(self.root)
      level += 1
    
    while(cq):
      cur = cq.popleft()
      if(isinstance(cur,Node)):
        #print cur.key
        current_level_key_list[item] = "{0}({1})".format(cur.key,cur.balanceFactor)

      if(cur == "NONE"):
          nq.append("NONE")
          nq.append("NONE")
      else:
        if(cur.lchild):
          non_none_flag = True
          nq.append(cur.lchild)
        else:
          nq.append("NONE")
          
        if(cur.rchild):
          non_none_flag = True
          nq.append(cur.rchild)
        else:
          nq.append("NONE")

      item += 1
      
      if(not cq):
        print Tree.get_key_line(Tree.height(self.root), level-1, current_level_key_list, 10)
        print "" 
        print "" 
        print "" 
          
        cq = nq
        nq = deque([])
        print "" 
        keys_per_level = int(math.pow(2, level-1))
        level += 1
        item = 0
        current_level_key_list = []
        for i in range(keys_per_level):
          current_level_key_list.append("NONE")

        if(not non_none_flag):
          break

        non_none_flag = False

    print ""
    print 30 * "="

  def __str__(self):
    return "Tree: [height: {0}, width: {1}]".format(self.height, self.width)

if __name__ == "__main__":

  n1 = Node(1)
  n2 = Node(2)
  n3 = Node(3)
  n4 = Node(4)
  n5 = Node(5)
  n6 = Node(6)
  n7 = Node(7)
  n8 = Node(8)
  n9 = Node(9)
  n20 = Node(20)

  #child rels
  n9.lchild = n20
  n7.rchild = n8
  n2.lchild = n4
  n2.rchild = n5
  
  n3.lchild = n6
  n3.rchild = n7

  n4.lchild = n9
  
  n1.lchild = n2
  n1.rchild = n3

  t = Tree()
  t.insert(n1)
  t.print_tree()
