def DFSBinaryOrdered(root, fcn, ltFcn):
    stack = [root]
    while len(stack) > 0:
        temp = stack.pop(0)
        if fcn(temp):
            return True
        if ltFcn(temp):
            if temp.getLeftBranch():
                temp.insert(0, temp.getLeftBranch())
        else:
            if temp.getRightBranch():
                temp.insert(0, temp.getRightBranch())
    return False
