'''
Created on 2011-10-09
Modified Python Recipe: http://code.activestate.com/recipes/522995/
@author: mavc
'''

from heapq import heapify, heappop, heappush
__all__ = ['PriorityDict']


class PriorityDict(dict):
    '''
    Implements a Min Heap with updateable priorities.
    From: http://code.activestate.com/recipes/522995/
    
    
    The basic idea is: we use a python dict to store all keys and values, while keeping
    a heap of (priority, key) pairs.
    
    The sorting order can be defined by passing in a key to the constructor, but the
    both keys and values should have __lt__ defined because of lexicographic sorting of tuples.
    
    Insertion: insert into dict, and insert into heap.
    Removal:   remove from dict ONLY. (keep in heap, rebuild when required).
    Update:    same as Insertion.
    
    '''

    def __init__(self, arg, key=None):
        '''
        Constructor for a PriorityDict
        '''
        super(PriorityDict, self).__init__(arg)
        
        if key is None:
            key = lambda x: x # the identity function
            
        self._key = key
        self._build_heap()

    def _build_heap(self):
        ''' Rebuild the heap '''
        key = self._key
        self._heap = [(key(v), v, k) for k, v in self.iteritems()]
        heapify(self._heap) # Heapify by key

    def min_item(self):
        ''' Get the item with the min value '''
        while self._heap:
            v, k = self._heap[0][1:]
            if k in self and self[k] == v:
                return (k, v)
            heappop(self._heap)

        raise IndexError()

    def min_key(self):
        ''' Get the key with the min value '''
        return self.min_item()[1]

    def pop_min_item(self):
        ''' Pops the item with the min value '''
        while self._heap:
            v, k = heappop(self._heap)[1:]
            if k in self and self[k] == v:
                del self[k]
                return (k, v)

        raise IndexError()

    def pop_min_key(self):
        ''' Pops the key with the min value '''
        return self.pop_min_item()[1]

    def __setitem__(self, key, value):
        super(PriorityDict, self).__setitem__(key, value)

        # Rebuild the heap if it gets too large.
        if len(self) < 2 * len(self._heap):
            heappush(self._heap, (self._key(value), value, key))
        else:
            self._build_heap()

    def update(self, *args, **kwargs):
        super(PriorityDict, self).update(*args, **kwargs)
        self._build_heap()


if __name__ == '__main__':

    priorities = [('A', 10), ('B', 50), ('C', 2), ('D', 20)]
    p = PriorityDict(priorities)

    print p   
    while p:
        print p.pop_min_item()
