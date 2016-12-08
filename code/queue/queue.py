
class Queue:

    def __init__(self):
        self.stacks = ([], [])
        self.reversed = False

    def _reverse(self):
        i, j = (0, 1) if self.reversed else (1, 0)
        while len(self.stacks[i]):
            self.stacks[i].pop()
        while len(self.stacks[j]):
            self.stacks[i].append(self.stacks[j].pop())
        self.reversed = not self.reversed

    def enqueue(self, item):
        if self.reversed:
            self._reverse()
        self.stacks[0].append(item)

    def dequeue(self):
        if self.reversed is False:
            self._reverse()
        return self.stacks[1].pop()


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
