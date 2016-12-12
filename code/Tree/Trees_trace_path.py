def TracePath(node):
    if not node.getParent():
        return [node]
    return [node] + TracePath(node.getParent())
