class myqueue:
    def __init__(self):
        self._contents = list()

    def __str__(self):
        return '{}'.format(self._contents[::-1])

    def __iter__(self):
        return iter(self._contents)

    def __len__(self):
        return len(self._contents)

    def enqueue(self, item):
        self._contents.append(item)

    def dequeue(self):
        last = None
        try:
            last = self._contents.pop(0)
        except Exception:
            print('Empty queue!')
        return last

    def front(self):
        return self._contents[0] if len(self) else None

    def back(self):
        return self._contents[-1] if len(self) else None

if __name__ == '__main__':
    q1 = myqueue()
    print(q1)
    print(len(q1))

    [q1.enqueue(x) for x in range(5)]
    print(q1)

    print('front:', q1.front())
    print('back:', q1.back())

    [print('dequeue:', q1.dequeue()) for _ in range(len(q1))]

    x = q1.dequeue()
    print('x:', x)
    print('back:', q1.back())
