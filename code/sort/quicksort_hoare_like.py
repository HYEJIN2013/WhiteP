def partition(A, p, r):
    i = p
    j = r
    m = A[i]
    while True:
        while A[j] > m and i < j:
            j -= 1
        if i < j:
            A[i], A[j] = A[j], A[i]
            i += 1
        while A[i] < m and i < j:
            i += 1
        if i < j:
            A[i], A[j] = A[j], A[i]
            j -= 1
        if i == j:
            break
    return i

def quicksort(A, p, r):
    # print(A, p, r, p < r)
    if p < r:
        q = partition(A, p, r)
        quicksort(A, p, q-1)
        quicksort(A, q+1, r)


from random import randrange
seq = [randrange(100000) for i in range(100000)]
import cProfile
cProfile.run('quicksort(seq, 0, len(seq)-1)')
