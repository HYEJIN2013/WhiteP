from UnionFind import unionfind
def kruskal(Ge, n):
    # Ge is a list of edges.
    # n is the number of vertices.
    Ge.sort(key=lambda x: x[2])
    Te = []
    uf = unionfind(n)
    for i, edge in enumerate(Ge):
        if not uf.connected(edge[0], edge[1]):
            Te.append(edge)
            uf.union(edge[0], edge[1])

    return Te
