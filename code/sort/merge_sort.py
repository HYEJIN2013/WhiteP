from heapq import merge
import random

def merge_sort(m):
    if len(m) <= 1:
        return m
 
    middle = len(m) / 2
    left = m[:middle]
    right = m[middle:]
 
    left = merge_sort(left)
    right = merge_sort(right)
    return list(merge(left, right))

def quick_sort(m):
  if len(m) <= 1:
    return m
  pivot = random.choice(m)
  smaller = [i for i in m if i < pivot]
  equal = [i for i in m if i == pivot]
  bigger = [i for i in m if i > pivot]
  return quick_sort(smaller) + equal + quick_sort(bigger)
