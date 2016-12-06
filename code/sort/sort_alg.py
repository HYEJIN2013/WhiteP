#!/usr/bin/env python

import profile
import random

from time import time

def insertion_sort(l):
    for i, x in enumerate(l):
        for j, y in enumerate(l[:i]):
            if x < y:
                l.insert(j, l.pop(i))
                break
    return l

def merge_sort(l):
    l, s, i = (insertion_sort(l[:len(l)/2]), insertion_sort(l[len(l)/2 + 1:len(l)])), [], 0
    while len(l[0]) and len(l[1]):
        if l[0][0] < l[1][0]:
            s.insert(i, l[0].pop(0))
        else:
            s.insert(i, l[1].pop(0))
        i += 1
    return s
    
if __name__ == "__main__":
    s = time()
    insertion_sort([random.randint(0, 1000) for i in range(1000)])
    print "Insertion Sort: {:.5}s".format(time() - s)
    
    s = time()
    merge_sort([random.randint(0, 1000) for i in range(1000)])
    print "Merge Sort: {:.5}s".format(time() - s)
