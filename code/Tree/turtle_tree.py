from turtle import *

speed(0)
lt(90) # start facing up

# l = start node length, m = node size multiplier, s = num of nodes
def tree(n, l=80, m=0.7, s=2):
	if n > 1:
		fd(l)
		rt(90) # start facing right

		a = 180 / (s + 1) # distribute nodes across 180 degrees

		for i in range(s):
			lt(a) # turn left
			fd(l * m) # draw node line
			tree(n - 1, l * m, m, s) # start a node
			bk(l * m) # return to node start
		rt(a * ((s - 1) / 2)) # return to center

		bk(l) # return to starting position

tree(6, l=50, s=4)

done()
