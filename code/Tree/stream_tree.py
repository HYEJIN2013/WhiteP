class Converging(object):
    def __init__(self, ds):
        self.ds = ds

    def diverge(self):
        self.ds.ds = None

class Node(object):
    def __init__(self, name):
        self.ds = None
        self.name = name
        
    def converge(self, ds):
        current = ds
        while current.ds:
            current = current.ds
        current.ds = self

        return Converging(current)

    def __gt__(self, node):
        node.converge(self)

    def __lt__(self, node):
        self.converge(node)

    def __str__(self):
        return self.name

    def chain_str(self):
        return self.name + ((' > %s' % self.ds.chain_str()) if self.ds else '')

a = Node('A')
b = Node('B')
c = Node('C')
d = Node('D')

a < b
c < d
a < c
print '--- finally ---'
print b.chain_str()
print d.chain_str()
