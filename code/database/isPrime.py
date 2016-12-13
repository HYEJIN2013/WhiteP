#!/usr/bin/env python
#
# Written by Winston Weinert (winston@ml1.net) on 28-March-2014
# This file is in the public domain.
#


try:
    xrange
except NameError:
    # Python 3 compatibility
    xrange = range


def sieve_of_eratosthenes(bottom, top=None):
    """
    Arbritary range Sieve of Eratosthenes.
    - If one argument, that argument serves as the ceiling.
    - If two arguments, the first is bottom, the second is ceiling.
    """

    if top is None:
        top, bottom = bottom, 2
    bottom = max(bottom, 2)

    sieve, p = set(xrange(bottom, top + 1)), 2
    while p is not None:
        next_p = None
        for n in frozenset(sieve):
            if n != p and n % p == 0:
                sieve.remove(n)
            elif p < n and next_p is None:
                next_p = n
        p = next_p

    return sieve


def isPrime():
    # 20th prime is 71.
    for prime in sieve_of_eratosthenes(71):
        print(prime)


if __name__ == '__main__':
    isPrime()
