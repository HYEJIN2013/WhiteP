import networkx as nx
import math
from random import shuffle
import matplotlib.pyplot as plt
# Binary search tree (BST)
# Dlya lubogo U iz left(t)
# Dlya lubogo V iz right(t)
# u < t < v
# bool isBST(t)
class Tree:
   def __init__(self, data, left=None, right=None):
      self.data = data
      self.left = left
      self.right = right
      self.parent = None
      self.is_black = True

      if self.left:
         self.left.parent = self

      if self.right:
          self.right.parent = self
   
   def __str__(self):
      return str(self.data)
   
   def nodes(self):
      #deeps first search
      yield from dfs_nodes(self)
   
   def __lt__( self, other ):
      return self.data < other.data

def is_black(node):
    return not node or node.is_black

def is_red(node):
    return not is_black(node)

def insert_rb_tree(tree, x):
    assert is_red_black(tree)
    node = insert(tree,x)
    if is_black( node.parent ):
        node.is_black = False
    
    assert is_red_black(tree)

def is_red_black(tree):
    pass

def next_node(bst):
   if bst.right:
      return min_node(bst.right)
   if not bst.parent or bst.parent.left == bst:
       return bst.parent

   while bst.parent and  bst.parent.right == bst:
       bst = bst.parent

   return bst.parent

def prev_node(bst):
   if bst.left:
      return max_node(bst.left)
   if bst.parent.right == bst:
       return bst.parent

   while bst.parent and bst.parent.left == bst:
       bst = bst.parent

   return bst.parent   

def end(bst):
   return None


def min_node(bst):
    assert bst is not None
    while bst.left:
        bst = bst.left
    return bst


def begin(bst):
    return min_node(bst)


def max_node(bst):
    assert bst is not None
    while bst.right:
        bst = bst.right
    return bst

def iterate(bst):
   it = begin(bst)
   while it != end(bst):
      yield it
      it = next_node(it)
   
def height(tree):
   if not tree:
      return 0
   else:
      return max(height(tree.left), height(tree.right)) + 1

def dfs_nodes(tree):
   if tree:
      yield from dfs_nodes( tree.left )
      yield tree
      yield from dfs_nodes( tree.right )

def bfs_nodes(tree):
   q = []
   q.append(tree)
   while q:
      node = q.pop(0)
      if node:
         yield node
         q.append(node.left)
         q.append(node.right)

def lower_bound( bst, x ):
   assert is_bst(bst)
   if bst:
      if x < bst.data:
         res = lower_bound( bst.left, x )
         if res:
            bst = res
      elif bst.data < x:
         return lower_bound( bst.right, x )
         
   return bst
   
   
def insert(tree,x):
   assert is_bst(tree)
   if x < tree.data:
      if tree.left:
         return insert(tree.left, x)
      else:
         tree.left = Tree(x)
         tree.left.parent = tree
         return tree.left
   elif tree.data < x:
      if tree.right:
         return insert(tree.right, x)
      else:
         tree.right = Tree(x)
         tree.right.parent = tree
         return tree.right
   return tree 
   
def traverse_preorder(tree, visitor):
   if tree:
      visitor( tree.data )
      traverse_preorder( tree.left, visitor )
      traverse_preorder( tree.right, visitor )

def traverse_inorder(tree, visitor):
   if tree:
      traverse_inorder(tree.left, visitor)
      visitor( tree.data )
      traverse_inorder( tree.right, visitor )

def traverse_postorder(tree, visitor):
   if tree:
      traverse_postorder( tree.left, visitor )
      traverse_postorder( tree.right, visitor )
      visitor(tree.data)

def traverse_bfs_rec( nodes, visitor ):
   nnodes=[]
   if len( nodes ) == 0:
      return
   for node in nodes:
      if node:
         visitor( node.data )
         nnodes.append( node.left )
         nnodes.append( node.right )
   traverse_bfs_rec( nnodes, visitor )
      
def traverse_bfs( tree, visitor ):
   nodes_to_visit = [tree]
   while( len(nodes_to_visit) ):
      node = nodes_to_visit.pop(0)
      if node:
         visitor( node.data )
         nodes_to_visit.append( node.left )
         nodes_to_visit.append( node.right )

def rotate_1(tree):
    pass

def remove(tree, x):
    pass
    
         
def is_bst(tree):
    prev = None
    for node in iterate(tree):
        if prev:
            if node < prev:
                return False
        prev = node
    return True

         
def create_tree_1():
    return Tree(10,
            Tree(4,
                Tree(3),
                Tree(5,
                    Tree(6))),
            Tree(20,
                Tree(15,
                    right=Tree(17,
                            Tree(16),
                            Tree(18, right=Tree(19))))))

def create_tree_2():
    return Tree(8,
            Tree(3,
                Tree(1),
                Tree(6,
                    Tree(4),
                    Tree(7))),
            Tree(10, 
                right=Tree(14,
                    Tree(13))))

def main():
    t = create_tree_2()
    print(is_bst(t))
    insert(t, 5)
    insert(t, 9)

    print(", ".join(map(str, iterate(t))))
    

if __name__ == "__main__":
   main()

# Red-black tree
# t - BST
# node can be red or black
# for any red node - left and right node are black
# for any leaf, route(root, leaf) has equal count of black nodes
# null node is black
# insert
# if parent is black - OK
# if uncle is black - swap with grand parent
# gp become left child
# 
