def bs(a, b):
    if a == b:
        return a
    if f(a) < 0:
        return bs((a+b) / 2, b)
    if f(b) > 0:
        return bs(a, (a+b) / 2)
    raise ValueError('something wrong :(')
