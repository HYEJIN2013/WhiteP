class Solution:
    # @param A, a list of integers
    # @param target, an integer to be searched
    # @return an integer
    def search(self, A, target):
        if len(A) == 0:
            return -1
        
        l = 0
        r = len(A) - 1
        while l + 1 < r:
            m = (l + r) >> 1
            head = A[l]
            if A[m] == target:
                return m
            elif head == target:
                return l
            elif A[m] > head:
                if target > A[m] or target < head:
                    l = m
                else:
                    r = m
            else:
                if target > head or target < A[m]:
                    r = m
                else:
                    l = m
        if A[l] == target:
            return l
        elif A[r] == target:
            return r
        else:
            return -1
