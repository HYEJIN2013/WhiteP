#hierarchies des noeuds
TREE = [None,'USER','PROJECT','RESOURCE','CORPUS','DOCUMENT']
#typeid, typename de mes noeuds
TREE_h = [(i, n) for i,n in enumerate(TREE)]

def asc_tree(self):
        '''Representation of the full ancestor tree hierarchy of the current node
        in a simple list
        '''
        tree = []
        pos = TREE.index(self.typename)
        #tree dependance stops to docs (pos 6)
        #are all children of corpus
        if pos > 6:
            pos = self.TREE.index('CORPUS')+1

        curr_node = self.id
        for i in range(pos):
            curr_node = self.parent_id
            tree.append(curr_node.id)
            curr_node = self.parent()
        return tree
