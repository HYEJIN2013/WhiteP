from __future__ import print_function
from collections import namedtuple


class Node(object):
    __slots__ = 'key left right parent'.split()

    def __init__(self, key=None, left=None, right=None, parent=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent

    def __str__(self):
        return '[{!r}] left:{!r} right:{!r} parent:{!r}'.format(
            self.key, self.left, self.right, self.parent)

    def __repr__(self):
        return '[{!r}]'.format(self.key)


class SplayTree:

    ''' Ref: http://zh.wikipedia.org/wiki/%E4%BC%B8%E5%B1%95%E6%A0%91 '''

    def __init__(self):
        self.root = None

#      y                           x
#     / \       Left Rotation    /  \
#    x   T3   < - - - - - - -   T1   y
#   / \                            / \
#  T1  T2                        T2   T3

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

#      x                           y
#     / \     Right Rotation     /  \
#    y   T3   - - - - - - - >   T1   x
#   / \                            / \
#  T1  T2                        T2   T3

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    def splay(self, x):
        ''' lift x up to root '''
        while x.parent:
            if not x.parent.parent:
                if x.parent.left == x:
                    self.right_rotate(x.parent)
                else:
                    self.left_rotate(x.parent)
            elif x.parent.left == x and x.parent.parent.left == x.parent:
                self.right_rotate(x.parent.parent)
                self.right_rotate(x.parent)
            elif x.parent.right == x and x.parent.parent.right == x.parent:
                self.left_rotate(x.parent.parent)
                self.left_rotate(x.parent)
            elif x.parent.left == x and x.parent.parent.right == x.parent:
                self.right_rotate(x.parent)
                self.left_rotate(x.parent)
            else:
                self.left_rotate(x.parent)
                self.right_rotate(x.parent)

    def find(self, v):
        ''' find v or the last visited position '''
        z = self.root
        p = None
        while z:
            p = z
            if v < z.key:
                z = z.left
            elif v > z.key:
                z = z.right
            else:
                return z
        return p

    def insert(self, v):
        ''' insert key v and splay this node (no duplicate) '''
        p = self.find(v)
        if p and p.key == v:
            return

        z = Node(key=v, left=None, right=None, parent=p)
        if not p:
            self.root = z
        elif v < p.key:
            p.left = z
        else:
            p.right = z
        self.splay(z)

    def replace(self, u, v):
        ''' replace u with v (can be none)
            deal with u's origin parent and root '''
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def minimum(self, u):
        while u.left:
            u = u.left
        return u

    def maximum(self, u):
        while u.right:
            u = u.right
        return u

    def delete(self, v):
        z = self.find(v)
        if not z or z.key != v:
            return
        self.splay(z)

        if not z.left:
            self.replace(z, z.right)
        elif not z.right:
            self.replace(z, z.left)
        else:
            y = self.minimum(z.right)
            if y.parent != z:
                self.replace(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.replace(z, y)
            y.left = z.left
            y.left.parent = y
        return z.key

    def show(self, node='root', prefix=0):
        if node == 'root':
            node = self.root
        print(' '*prefix + str(node))
        if node:
            self.show(node.left, prefix+2)
            self.show(node.right, prefix+2)

if __name__ == '__main__':
    import random
    t = SplayTree()
    l = range(10)
    random.shuffle(l)
    for i in l:
        t.insert(i)
    print('l:', l)
    print('after insertion:')
    t.show()
    v = t.delete(t.root.key)
    print('after delete {}:'.format(v))
    t.show()
