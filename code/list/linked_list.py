from heapq import heappop, heappush, heapify

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

    def __str__(self):
        return "<Node: %d>" % self.val

class LL(object):
    def __init__(self):
        self.first = None
        self._n = 0

    def insert(self, val):
        node = Node(val)
        if self.first is None:
            self.first = node
            self._n += 1
            return

        cur = self.first
        while not cur.next is None:
            cur = cur.next

        cur.next = node
        self._n += 1

    def ith_from_val(self, val, i):
        if i < 0: raise Exception("Cannot search with negative numbers")

        cur = self.first
        found = self.first

        # Iterate i positions next for value to search
        while i > 0:
            i -= 1
            cur = cur.next

            # Fell of the end looking for ith position
            if cur is None: return None

        # Iterate till value is found
        while cur.val != val:
            cur = cur.next
            found = found.next

            # Value not in list
            if cur is None: return None

        return found

    def ith_smallest_val(self, val, i):
        # Find node for the value
        node = self.find_node(val)
        if node is None: return None

        cur = self.first

        heap = []
        heapify(heap)
        # Create a min priority queue vals smaller than
        # requested val
        while not cur.next is None:
            if cur.val < node.val:
                heappush(heap, cur.val)
            cur = cur.next

        # If the length of the heap is not ith big
        # Then then ith value smallest is not in the heap
        if len(heap) < i: return None

        val = None
        # set val as smallest val in heap until
        # length of heap - i is found
        while len(heap) - i >= 0:
            val = heappop(heap)
        return val

    def find_node(self, val):
        node = self.first
        # Iterate till node is found or None
        while node.val != val:
            node = node.next
            # Node not found
            if node is None: return None
        return node

    def __len__(self):
        return self._n

    def __str__(self):
        return "<LL has %d nodes>" % len(self)

if __name__ == "__main__":
    ll = LL()

    for i in range(1, 11):
        ll.insert(i)

    print ll.ith_from_val(10, 8) # Found
    print ll.ith_from_val(1, 0) # Found
    print ll.ith_from_val(2, 1) # Found
    print ll.ith_from_val(4, 8) # Not found ith
    print ll.ith_from_val(1, 20) # Not found val
    print ll.ith_from_val(10, 10) # not found ith
    #print ll.ith_from_val(5, -1) # exception

    print "ith smallest val...."

    print ll.ith_smallest_val(5, 2) # finds 2 smaller 3
    print ll.ith_smallest_val(3, 4) # cant find smaller
    print ll.ith_smallest_val(11, 2) # value not found
