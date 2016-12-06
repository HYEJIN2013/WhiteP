import sys

s = {}

for i in range(1, 6):
	s[i] = sys.maxsize

for i in range(5):
    
    while True:
    	try:
    		x = raw_input('Enter int #%s: ' %i)
    		x = int(x)
    		break
    	except ValueError:
    		print 'You must enter a valid integer.'
    
    if x < s[1]:
        s[5] = s[4]
        s[4] = s[3]
        s[3] = s[2]
        s[2] = s[1]
        s[1] = x
    elif x < s[2]:
        s[5] = s[4]
        s[4] = s[3]
        s[3] = s[2]
        s[2] = x
    elif x < s[3]:
        s[5] = s[4]
        s[4] = s[3]
        s[3] = x
    elif x < s[4]:
        s[5] = s[4]
        s[4] = x
    elif x < s[5]:
        s[5] = x

for i in range(1, 6):
	print s[i]
