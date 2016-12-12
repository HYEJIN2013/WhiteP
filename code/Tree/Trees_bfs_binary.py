def BFSBinary(root, fcn):
    queue = [root]
    while len(queue):
        if fcn(queue[0]):
            return True
        temp = queue.pop(0)
        if temp.getLeftBranch():
            queue.append(temp.getLeftBranch())
        if temp.getRightBranch():
            queue.append(temp.getRightBranch())
    return False
