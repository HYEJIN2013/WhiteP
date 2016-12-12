#!/usr/bin/env python
from nltk.tree import ParentedTree

class Constituent(ParentedTree):
    def __init__(self, node, children=None):
        self.head_word = None
        self.start = None
        self.end = None
        super(Constituent, self).__init__(node, children)

    def terminal(self):
        return isinstance(self[0], str)

    def nonterminal(self):
        return not isinstance(self[0], str)

    def build_index(self, start):
        if self.terminal():
            self.start = start
            self.end = start+ 1
        else:
            self.start = start
            for kid in self:
                kid.build_index(start)
                start = kid.end
            self.end = self[-1].end


import unittest
class ConstituentUnittest(unittest.TestCase):
    def setUp(self):
        tkn = "(S1 (S (NP (NNP Ms.) (NNP Haag)) (VP (VBZ plays) (NP (NNP Elianti))) (. .)))"
        self.t = Constituent.fromstring(tkn)
        self.t.build_index(0)

    test1 = lambda self: self.assertEqual("S1", self.t.label())
    test2 = lambda self: self.assertTrue(self.t[0].nonterminal())
    test3 = lambda self: self.assertTrue(self.t[0][0][0].terminal())
    test4 = lambda self: self.assertEqual(0, self.t[0].start)
    test5 = lambda self: self.assertEqual(5, self.t[0].end)
    test6 = lambda self: self.assertEqual(2, self.t[0][1].start)
    test7 = lambda self: self.assertEqual(4, self.t[0][1].end)

if __name__=="__main__":
    unittest.main()
