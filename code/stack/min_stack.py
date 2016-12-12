class MinStack:
    
    def __init__(self):
        self.data = []
        self.mins = []

    # @param x, an integer
    def push(self, x):
        self.data.append(x)
        if self.mins == [] or self.mins[-1] >= x:
            self.mins.append(x)

    # @return an integer
    def pop(self):
        if not self.data:
            return -1
        x = self.data.pop()
        
        if self.mins and self.mins[-1] == x:
            self.mins.pop()
        return x


    # @return an integer
    def top(self):
        if not self.data:
            return -1
        return self.data[-1]

    # @return an integer
    def getMin(self):
        if not self.data:
            return -1
        return self.mins[-1]
