#!/usr/local/bin/python2.7

import string
import itertools

x = list(xrange(100))
y = string.lowercase[:26]

z= [x[n:n+3] for n,m in enumerate(x) if not (n % 3)]
joe = list( itertools.izip_longest(z,y, fillvalue=""))
map(lambda x:x[0].append(x[1]), joe)
result = [j[0] for j in joe]
final = [x for x in reduce(lambda x,y: x+y, result) if x != '']
print final
