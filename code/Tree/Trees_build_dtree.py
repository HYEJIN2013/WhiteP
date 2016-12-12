def buildDTree(sofar, todo):
    here = binaryNode(sofar)
    if len(todo) == 0:
        return here
    withelt = buildDTree(sofar + [todo[0]], todo[1:])
    withoutelt = buildDTree(sofar, todo[1:])
    here.setLeftBranch(withelt)
    here.setRightBranch(withoutelt)
    return here
