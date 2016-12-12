class stack:
    def __init__(self):
        self._contents = list()

    def __str__(self):
        return '{}'.format(self._contents[::-1])

    def __len__(self):
        return len(self._contents)

    def push(self, item):
        self._contents.append(item)

    def pop(self):
        top = None
        try:
            top = self._contents.pop()
        except Exception:
            print('Empty stack!')
        return top

    def peek(self):
        return self._contents[-1] if len(self) else None

if __name__ == '__main__':
    s1 = stack()
    print(s1)
    print(len(s1))

    [s1.push(x) for x in range(3)]
    print(s1)

    [print('pop:', s1.pop()) for _ in range(len(s1))]

    x = s1.pop()
    print('x:', x)

    print('peek', s1.peek())
