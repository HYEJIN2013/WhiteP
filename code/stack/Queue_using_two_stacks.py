
class Queue:

    def __init__(self):
        self.stack1 = []
        self.stack2 = []
        self.reversed = False

    def enqueue(self, item):
        if self.reversed is False:
            self.stack1.append(item)
        else:
            while len(self.stack1):
                self.stack1.pop()
            while len(self.stack2):
                self.stack1.append(self.stack2.pop())
            self.reversed = False
            self.stack1.append(item)

    def dequeue(self):
        if self.reversed is False:
            while len(self.stack2):
                self.stack2.pop()
            while len(self.stack1):
                self.stack2.append(self.stack1.pop())
            self.reversed = True
            return self.stack2.pop()
        else:
            return self.stack2.pop()


q = Queue()
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
print q.dequeue()
print q.dequeue()
q.enqueue(4)
print q.dequeue()
print q.dequeue()
# Should print 1,2,3,4
