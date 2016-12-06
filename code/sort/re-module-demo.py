# http://blog.abhranil.net/2013/05/18/python-script-word-frequency-counter/
from re import compile
l=compile("([\w,.'\x92]*\w)").findall(open(raw_input('Input file: '),'r').read().lower())
f=open(raw_input('Output file: '),'w')
print l
d = {}
for word in set(l):
    print>>f, word, '\t', l.count(word)
    d[word] = l.count(word)

f.close()

list =[]
for w in sorted(d,key=d.get,reverse=True):
    print w,d[w]
    list.append((w,d[w]))

print "the most used words is \'",list[0][0] ,"\' and it appear ",list[0][1] ," times"
