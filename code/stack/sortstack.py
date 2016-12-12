from stack import stack

def sort(unsorted):
    sortedStack = stack()

    while len(unsorted):
        top = unsorted.pop()
        while len(sortedStack) and sortedStack.peek() < top:
            unsorted.push(sortedStack.pop())
        sortedStack.push(top)

    return sortedStack

if __name__ == '__main__':
    s1 = stack()
    print(sort(s1))

    [s1.push(i) for i in (-10.5, 48.3, -7.1, 19.23, -8, -10.5)]

    s2 = sort(s1)
    print(s2)
