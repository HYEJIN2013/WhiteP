class Stack(object):
    def __init__(self):
        self.N = 0
        self.s = [None]*2
    def isEmpty(self):
        return self.N == 0
    def size(self):
        return self.N
    def resize(self,capacity):
        assert capacity >= self.N
        for i in range(slef.N):
            temp[i] = self.s[i]
        self.s =temp
    def push(self,item):
        if self.N == len(self.s):
            resize(2*len(self.s))
        self.s.append(item)
        self.N +=1
    def pop(self):
        if self.isEmpty:
            return
        else:
            result = self.s[N-1]
            N -=1
            if N >0 and N == len(self.s)/4:
                resize(len(self.s)/2)
            return result
    def peek(self):
        return self.s[N-1]
        
        
        
class Tower:
  
    def __init__(self,i):
        self.index = i
        self.disks = Stack()
        
    def add(self,d):
        if self.disks.isEmpty() and slef.disks.peek() <= d:
            raise ValueError
        else:
            self.disks.push(d)
            
    def index(self):
        return self.index
        
    def moveTopTo(self,t):
        top = self.disks.pop()
        t.add(top)
        print "Move disk ", top,  " from " , index(), " to ", t.index()
        
    def mes_print(self):
        print "contents of Tower " , self.index()
        i=disks.size()-1
        while i >=0:
            print " " , disks.get(i)
            i -=1
            
    def moveDisks(self,n,dest,t_buffer):
        if n >0:
            self.moveDisks(n-1, t_buffer,dest)
            self.moveTopTo(dest)
            t_buffer.moveDisks(n-1,dest,self)
            
            
if __name__ =="__main__":
    n =5
    towers = [None]*n
    for i in range(3):
        towers[i]= Tower[i]
    j = n-1
    while j >=0:
        towers[0].add(j)
        towers[0].moveDisks(n,towers[2],towers[1])
