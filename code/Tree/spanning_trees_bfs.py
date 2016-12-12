"""
return any spanning tree out of a graph.
"""
from collections import deque


def spanning_tree(graph):
    # graph is a list of lists
    root = 0
    tree = [[] for x in xrange(len(graph))]
    queue = deque([root])
    visited = set()
    while queue:
        node = queue.pop()
        visited.add(node)
        for x in graph[node]:
            if x not in visited:
                queue.appendleft(x)
                tree[node].append(x)
                visited.add(x)
    return tree
