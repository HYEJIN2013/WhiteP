def DFSBinary(root, fcn):
    stack = [root]
    while len(stack) > 0:
        if fcn(stack[0]):
            return True
        temp = stack.pop(0)
        if temp.getRightBranch():
            stack.insert(0, temp.getRightBranch())
        if temp.getLeftBranch():
            stack.insert(0, temp.getLeftBranch())
    return False
