import unittest
from elementary import *
from mrgsort import *

class Test(unittest.TestCase):

    def setUp(self):
        self.test = [4,2,6,8,3,1,9,10,27,89,2]
        self.output = [1,2,2,3,4,6,8,9,10,27,89]

    def test_selection(self):
        self.assertEquals(selection(self.test),self.output)

    def test_insertion(self):
        self.assertEquals(insertion(self.test),self.output)

    def test_shell(self):
        self.assertEquals(shellsort(self.test),self.output)

    def test_mrgsort(self):
        self.assertEquals(mergesort(self.test),self.output)

    def test_qsort(self):
        self.assertEquals(quicksort(self.test),self.output)

if __name__ == "__main__":
    unittest.main()
