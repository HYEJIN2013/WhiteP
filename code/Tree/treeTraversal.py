#different tree traversal method WORK IN PROGRESS

# breadth-first: queue 
def BFS(node):
  queue=dequeue([])
  queue.append(node)
  while not queue:
    currNode= queue.popleft()
    print currNode.value
    if currNode.leftChild:
        queue.append(currNode.leftChild)
    if currNode.rightChild:
        queue.append(currNode.rightChild)

# depth-frist: recursion
def DFS(node,method):
  # in-order
  if method='INORDER':
    DFS(node.leftChild,"INORDER")
    print node.value
    DFS(node.rightChild,"INORDER")
    
  # pre-order
  if method="PREORDER":
    print node.value
    DFS(node.leftChild,"PREORDER")
    DFS(node.rightChild,"PREORDER")
    
  # post-order
  if method= "POSTORDER":
    DFS(node.leftChild,"POSTORDER")
    DFS(node.rightChild,"POSTORDER")
    print node.value
  
  #linear preorder
  if method = "LINEAR":
    stack=[]
    stack.append(node)
    while not stack:
        n=stack.pop()
        print n.value
        if n.rightChild:
            stack.append(n.rightChild)
        if n.leftChild:
            stack.append(n.leftChild)
            
        
#triangular work in progress, 
def printTriangular(root,flag,toPrint):
    if not node.parent:
      print node.value
      if node.leftChild:printTriangular(node.leftChild,'preOrder',True)
      if node.rightChild:printTriangular(node.rightChild,'postOrder',True)
    else:
        #left
        if flag is 'preOrder'
          if (not node.rightChild and not node.leftChild)
          or toPrint:
              print node.value
          if node.leftChild:printTriangular(node.leftChild,flag,toPrint)
          if node.rightChild:printTriangular(node.rightChild,flag,False)
        #right
        if flag is 'postOrder':
          if node.leftChild:printTriangular(node.leftChild,flag,False)
          if node.rightChild:printTriangular(node.rightChild,flag,toPrint)
          if (not node.rightChild and not node.leftChild) or toPrint:
              print node.value
          
