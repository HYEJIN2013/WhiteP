from networkx import Graph
from networkx.exception import NetworkXException, NetworkXError
import networkx.convert as convert

class Tree(Graph):
    """ A free (unrooted) tree."""
    def __init__(self, data=None, **attr):
        Graph.__init__(self, **attr)
        if data is not None:
            convert.to_networkx_graph(data, create_using=self)
            # check if it is a tree.
            if not (G.order() == G.size() + 1 and
                    nx.number_connected_components(G) == 1):
                raise NetworkXError("Data %s is not a tree" % data)
        # load graph attributes (must be after convert)
        self.graph.update(attr)
        self.edge = self.adj

    def add_node(self, n):
        if n in self:
            return  # already in tree
        elif len(self.adj) == 0:
            Graph.add_node(self, n)  # first node
        else:  # not allowed
            raise NetworkXError(
                "adding single node %s not allowed in non-empty tree" % (n))

    def add_nodes_from(self, nbunch):
        for n in nbunch:
            self.add_node(n)

    def remove_node(self, n):
        try:
            if len(self.adj[n]) == 1:  # allowed for leaf node
                Graph.remove_node(self, n)
            else:
                raise NetworkXError(
                    "deleting interior node %s not allowed in tree" % (n))
        except KeyError:  # NetworkXError if n not in self
            raise NetworkXError("node %s not in graph" % n)

    def remove_nodes_from(self, nbunch):
        for n in nbunch:
            self.remove_node(n)

    def add_edge(self, u, v=None):
        if v is None:
            (u, v) = u  # no v given, assume u is an edge tuple
        if self.has_edge(u, v):
            return  # no parallel edges allowed
        elif u in self and v in self:
            raise NetworkXError(
                "adding edge %s-%s not allowed in tree" % (u, v))
        elif u in self or v in self:
            Graph.add_edge(self, u, v)
            return
        elif len(self.adj) == 0:  # first leaf
            Graph.add_edge(self, u, v)
            return
        else:
            raise NetworkXError(
                "adding edge %s-%s not allowed in tree" % (u, v))

    def add_edges_from(self, ebunch):
        for e in ebunch:
            self.add_edge(e)

    def remove_edge(self, u, v=None):
        if v is None:
            (u, v) = u
        if self.degree(u) == 1 or self.degree(v) == 1:  # leaf edge
            Graph.remove_edge(self, u, v)
        else:  # interior edge
            raise NetworkXError(
                "deleting interior edge %s-%s not allowed in tree" % (u, v))
        if self.degree(u) == 0:  # OK to remove remaining isolated node
            Graph.remove_node(self, u)
        if self.degree(v) == 0:  # OK to remove remaining isolated node
            Graph.remove_node(self, v)

    def remove_edges_from(self, ebunch):
        for e in ebunch:
            self.remove_edge(e)

    # leaf notation
    def add_leaf(self, u, v=None):
        self.add_edge(u, v)

    def remove_leaf(self, u, v=None):
        self.remove_edge(u, v)

    def add_leaves_from(self, ebunch):
        for e in ebunch:
            self.add_leaf(e)

    def remove_leaves_from(self, ebunch):
        for e in ebunch:
            self.remove_leaf(e)
