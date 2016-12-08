class tree(object):
    def __init__(self, name, children = [], parent = None):
        self.name = name
        self.children = children
        self.parent = parent
            
    def setChildren(self, children):
        self.children = children
    
    def setParent(self, parent):
        self.parent = parent
    
    def getName(self):
        return self.name
        
    def getParent(self):
        return self.parent
        
    def getChildren(self):
        return self.children  
          
    def __str__(self, level=0):
        ret = "\t"*level+str(self.name)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret
        
                        
def depthFirst(tree, name):
    """Searches for the node - name in the tree.
    returns the node if name is in the tree
    else, returns None
    tree: a tree object
    name: a str
    """
    queue = [tree]
    while len(queue) > 0:
        print "Now Searching: ", queue[0].getName()
        if queue[0].getName() == name:
            return queue[0]
        else:
            temp = queue.pop(0)
            if len(temp.getChildren()) > 0:
                children = temp.getChildren()[::-1]
                for child in children:
                    queue.insert(0, child)
                    
#T1 = tree("a", [tree("b", [tree("d"),tree("e"),tree("f")]), tree("c", [tree("g", [tree("h")])])])

#print depthFirst(T1, "g").getName()

#print T1
