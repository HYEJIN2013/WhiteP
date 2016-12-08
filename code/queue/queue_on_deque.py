from deque import *



class Queue(Deque):

    def __init__(self):

        Deque.__init__(self)



    def isEmpty(self):

        return Deque.isEmpty(self)



    def size(self):

        return Deque.size(self)



    def dequeue(self,item):

        Deque.addRear(self,item)



    def enqueue(self):

        return Deque.removeFront(self)
