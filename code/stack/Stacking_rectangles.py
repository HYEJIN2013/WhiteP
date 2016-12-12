def lcs(x, y):
    n = len(x)
    m = len(y)
    table = dict()  # a hashtable, but we'll use it as a 2D array here

    for i in range(n+1):      # i=0,1,...,n
        for j in range(m+1):  # j=0,1,...,m
            if i == 0 or j == 0:
                table[i, j] = 0
            elif x[i-1] == y[j-1]:
                table[i, j] = table[i-1, j-1] + 1
            else:
                table[i, j] = max(table[i-1, j], table[i, j-1])

    return table[n, m]

# If we put all the widths and heights of the rectangles into two sorted list,
# the problem is solved by simply calculating the longest common subsequence of
# the sequences of original indexes of the two lists.
def stack(rects):
    def get_sorted_indexes(idx):
        # Generates the sequence of the original indexes according to
        # the widths (when idx==0) and heights (when idx==1).
        # i.e. [0, 1, 2, 3, 4] and [3, 4, 0, 1, 2] from
        # [(1, 10), (2, 11), (3, 12), (4, 4), (5, 5)]
        tmp = sorted([ (i, r[idx]) for i, r in enumerate(rects) ],
                key=lambda x: x[1])
        return [ x[0] for x in tmp ]
    print lcs(get_sorted_indexes(0), get_sorted_indexes(1))

if __name__=="__main__":
    stack( [(2,2), (7, 15), (5, 8), (8, 5), (30, 30)] ) # print 4
    stack( [(1, 10), (2, 11), (3, 12), (4, 4), (5, 5)] ) # print 3
