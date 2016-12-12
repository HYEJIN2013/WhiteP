from collections import deque


# push O(n)
# top, pop, O(1)
class Stack1:
    # initialize your data structure here.
    def __init__(self):
        self.q = deque()

    # @param x, an integer
    # @return nothing
    def push(self, x):
        n = len(self.q)
        self.q.append(x)
        for i in range(n):
            self.q.append(self.q.popleft())

    # @return nothing
    def pop(self):
        self.q.popleft()

    # @return an integer
    def top(self):
        return self.q[0]

    # @return an boolean
    def empty(self):
        return not self.q


# push O(1)
# top, pop O(n)
class Stack2:
    # initialize your data structure here.
    def __init__(self):
        self.q = deque()

    # @param x, an integer
    # @return nothing
    def push(self, x):
        self.q.append(x)

    # @return nothing
    def pop(self):
        n = len(self.q)
        for i in range(n-1):
            tmp = self.q.popleft()
            self.q.append(tmp)
        self.q.popleft()

    # @return an integer
    def top(self):
        n = len(self.q)
        for i in range(n):
            tmp = self.q.popleft()
            self.q.append(tmp)
        return tmp

    # @return an boolean
    def empty(self):
        return not self.q
