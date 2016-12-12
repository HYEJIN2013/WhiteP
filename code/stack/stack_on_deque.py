from deque import *

class stack(Deque):

    def __init__(self):
        Deque.__init__(self)

    def isEmpty(self):
        return Deque.isEmpty(self)

    def size(self):
        return Deque.size(self)

    def push(self,item):
        Deque.addFront(self,item)

    def pop(self):
        return Deque.removeFront(self)
