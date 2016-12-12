def DFSBinaryPath(root, fcn):
    stack = [root]
    while len(stack) > 0:
        temp = stack.pop(0)
        if fcn(temp):
            return TracePath(temp)
        if temp.getRightBranch():
            stack.insert(0, temp.getRightBranch())
        if temp.getLeftBranch():
            stack.insert(0, temp.getLeftBranch())
    return False
