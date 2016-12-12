class Node(object):
    def __init__(self, x):
        self.val = x
        self.next = None
        self.count = 0

#s1 = push(5, s0)    #(5,1)
#s2 = push(6, s1)    #(6,2)->(5,1)
#s3 = push(7, s0)    #(7,3)->(6,2)->(5,1)

def push(num, node):
    newNode = Node(num)
    if node is None:
        newNode.next = None
        newNode.count = 1
    else:
        newNode.next = node
        newNode.count = node.count + 1
    return newNode

def pop(node):
    if node is None:
        return None
    node = node.next
    return node

def size(node):
    if node is None:
        return 0
    return node.count

def peek(node):
    if node is None:
        return None
    return node.val


import unittest
class TestPersistent(unittest.TestCase):
    def test_push_returns_head_1(self):
        s0 = None
        s1 = push(5, s0)
        self.assertEqual(s1.val, 5)

    def test_push_returns_head_2(self):
        s0 = None
        s1 = push(5, s0)
        s2 = push(6, s1)
        s3 = push(7, s2)
        self.assertEqual(s2.val, 6)
        self.assertEqual(s3.val, 7)
        isvalid = True
        curr = s3
        cntr = 0
        validator = [7, 6, 5]
        while curr:
            if(curr.val != validator[cntr]):
                isvalid = False
            cntr += 1
            curr = curr.next
        self.assertEqual(isvalid, True)

    def test_pop_returns_remaining_nodes(self):
        s0 = None
        s1 = push(5, s0)
        s2 = push(6, s1)
        s3 = push(7, s2)
        s4 = pop(s3)
        self.assertEqual(s4.val, 6)
        isvalid = True
        curr = s4
        cntr = 0
        validator = [6, 5]
        while curr:
            if(curr.val != validator[cntr]):
                isvalid = False
            cntr += 1
            curr = curr.next
        self.assertEqual(isvalid, True)


    def test_peek_returns_correct(self):
        s0 = None
        s1 = push(5, s0)
        s2 = push(6, s1)
        s3 = push(7, s2)
        self.assertEqual(peek(s3), 7)
        self.assertEqual(peek(s2), 6)

    def test_size_returns_lenght_of_linked_list(self):
        s0 = None
        s1 = push(5, s0)
        s2 = push(6, s1)
        s3 = push(7, s2)
        self.assertEqual(size(s3), 3)
        self.assertEqual(size(s2), 2)

if __name__ == "__main__":
    unittest.main()



# s1 : node1
#       5
# s2 : node2 -> node1
#       6        5
# s3 : node3 -> node2 -> node1
#       7        6        5
# s4 : node2 -> node1
# pop(s4) -> 6->5
# pop(s2) -> 5

#s0 = None
#s1 = push(5, s0)    #5
#s2 = push(6, s1)    #6->5
#s3 = push(7, s0)    #7
#s4 = push(8, s2)    #8->6->5

#
# Your previous Plain Text content is preserved below:
#
# // Implement a persistent (i.e. immutable) stack data structure with
# // the following interface:
#
# type stack of integers
#
# empty   : () -> stack  // i.e. a constructor
# size    : stack -> int
# peek    : stack -> int // returns the most recently pushed element
# *push   : (int, stack) -> stack
# *pop    : stack -> stack
#
# s0 = empty()
# s1 = push(5, s0) // 5
# s2 = push(6, s1) // 6, 5
# s3 = push(7, s1) // 7, 5
# s4 = pop(s3) // 5
#
# assert size(s0) == 0
# assert peek(s1) == 5
# assert size(s1) == 1
# assert peek(s2) == 6
# assert size(s2) == 2
# assert peek(s3) == 7
# assert size(s3) == 2
# assert peek(s4) == 5
# assert size(s4) == 1
#
