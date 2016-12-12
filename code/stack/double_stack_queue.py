# !/usr/bin/python
# -*- encoding: utf-8 -*-

class DoubleStackQueue:

    def __init__(self):
        self.first_stack = []
        self.second_stack = []

    def en_queue(self, el = None):
        self.first_stack.append(el)

    def de_queue(self):
        if len(self.second_stack) == 0:
            while len(self.first_stack) != 0:
                self.second_stack.append(self.first_stack.pop())
        return self.second_stack.pop()

if __name__ == '__main__':
    queue = DoubleStackQueue()
    queue.en_queue(1)
    queue.en_queue(2)

    print queue.de_queue()
    print queue.de_queue()

    queue.en_queue(3)
    print queue.de_queue()

    print queue.de_queue()
