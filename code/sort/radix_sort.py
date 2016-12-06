base = 10

def radix_sort(x, max):
    radix = 1
    while radix < max:
        x = counting_sort(x, radix)
        radix *= base
    return x

def counting_sort(a, radix):
    c = [0] * base
    for k in a:
        r = (k / radix) % base
        c[r] += 1

    for i in range(1, base):
        c[i] += c[i - 1]

    b = [0] * len(a)
    for k in reversed(a):
        r = (k / radix) % base
        b[c[r] - 1] = k
        c[r] -= 1

    return b

print radix_sort([925, 663, 212, 58, 775, 802], 1000)
