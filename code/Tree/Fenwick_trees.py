#!/usr/bin/env python3


class Fenwick:
    """A specialized data structure for representing range sums."""

    def __init__(self, size, identity=0):
        self.tree = [identity] * (size + 1)
        self.identity = identity

    @classmethod
    def from_list(cls, items, identity=0):
        self = cls(len(items), identity)
        for i, x in enumerate(items):
            self.increase(i, x)
        return self

    def increase(self, index, delta):
        i = index + 1
        while i < len(self.tree):
            self.tree[i] += delta
            i += -i & i

    def query(self, index):
        result = self.identity
        i = index
        while i > 0:
            # The ordering of the below expression is very important
            # when ``+`` is non-commutative
            result = self.tree[i] + result
            i -= -i & i
        return result

    def query_slice(self, start, end):
        return self.query(end) - self.query(start)

    def __repr__(self):
        return '<Fenwick {!r}>'.format(self.tree)


if __name__ == '__main__':
    nums = list(range(1, 11))
    f = Fenwick.from_list(nums)
    print(f)
    for i in range(len(nums)+1):
        print(f.query(i))
