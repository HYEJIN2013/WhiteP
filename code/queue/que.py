import queue as	q
que = q.Queue()
l = ""
while l	!= "end":
    l =	input("Add to q: ")
    que.put(l)
    if l == "end":
        while not que.empty():
            print(que.get())
