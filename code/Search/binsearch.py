def binsearch(l, term):
    bottom = 0
    top = len(l)
    middle = (bottom + top) // 2
    if term < l[middle]:
        return binsearch(l[:middle], term)
    elif term > l[middle]:
        return binsearch(l[middle:], term)
    elif term == l[middle]:
        return middle
