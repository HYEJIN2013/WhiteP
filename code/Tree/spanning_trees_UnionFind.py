import array


class unionfind:
    def __init__(self, n):
        self._length = n
        self._roots = array.array('L', [x for x in xrange(n)])
        self._weights = array.array('L', [1]*n)

    def __str__(self):
        return str(self._roots)

    def union(self, a, b):
        assert isinstance(a, int) and isinstance(b, int)
        assert a < self._length and b < self._length

        aroot = self.find(a)
        broot = self.find(b)
        if self._weights[aroot] > self._weights[broot]:
            self._roots[broot] = aroot
            self._weights[aroot] += self._weights[broot]
            self._weights[broot] = 0
        else:
            self._roots[aroot] = broot
            self._weights[broot] += self._weights[aroot]
            self._weights[aroot] = 0

    def connected(self, a, b):
        assert isinstance(a, int) and isinstance(b, int)
        assert a < self._length and b < self._length

        return self.find(a) == self.find(b)

    def find(self, a):
        assert isinstance(a, int)

        while self._roots[a] != a:
            self._roots[a] = self._roots[self._roots[a]]
            a = self._roots[a]

        return a
