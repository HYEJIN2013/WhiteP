'''
From Python Algorithms - Mastering Basic Algorithms in the Python Language Book
'''
def partition(seq):
    pi, seq = seq[0], seq[1:]         # Pick and remove the pivot
    lo = [x for x in seq if x <= pi]  # All the small elements
    hi = [x for x in seq if x > pi]   # All the large ones
    return lo, pi, hi                 # pi is "in the right place"


def quicksort(seq):
    if len(seq) <= 1:                            # Base case
        return seq
    lo, pi, hi = partition(seq)                  # pi is in its place
    return quicksort(lo) + [pi] + quicksort(hi)  # Sort lo and hi separately

from random import randrange
seq = [randrange(1000) for i in range(100000)]
import cProfile
cProfile.run('quicksort(seq)')
