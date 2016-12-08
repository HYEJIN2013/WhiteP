import timeit
code_list = """
import random
l = [random.randint(1, 1000) for _ in range(1000)]
que = list()
for x in l: que.append(x)
for _ in range(1000): que.pop(0)
"""
code_deque = """
import collections, random
que = collections.deque()
l = [random.randint(1, 1000) for _ in range(1000)]
for x in l: que.append(x)
for _ in range(1000): que.popleft()
"""
code_Queue = """
import queue, random
que = queue.Queue()
l = [random.randint(1, 1000) for _ in range(1000)]
for x in l: que.put(x)
for _ in range(1000): que.get()
"""
print('{:20}{:.3f}s'.format('list:', timeit.timeit(stmt=code_list, number=1000)))
print('{:20}{:.3f}s'.format('collections.deque:', timeit.timeit(stmt=code_deque, number=1000)))
print('{:20}{:.3f}s'.format('queue.Queue:', timeit.timeit(stmt=code_Queue, number=1000)))
