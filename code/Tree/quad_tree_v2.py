def f(i):
    x = next(i)
    if x == 'x':
        a, b, c, d = [f(i)for _ in'-'*4]
        x += c + d + a + b
    return x
for _ in range(input()):print f(iter(raw_input()))
