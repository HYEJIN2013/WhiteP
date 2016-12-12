# -*- coding: utf-8 -*-
#not fully working atm
import os
import os.path
import math
import sys

def dir_size(dir):
    total = 0
    for dirpath, dirnames, filenames in os.walk(dir):
        for x in filenames:
            y = os.path.join(dirpath, x)
            total += os.path.getsize(y)
    return total

def file_size(file):
	'''return file size in mb'''
	try:
		return ((os.stat(file).st_size)*math.pow(10, -4))
	except:
		return 0

def tree(directory, indentation):
	'''show up the tree'''
	print("%s%s:" % (indentation, directory))
	try:
		for filename in os.listdir(directory):
			print("%s|%s %i ko" % (indentation, filename, file_size(filename)))
		for filename in os.listdir(directory):
			subitem = os.path.join(directory, filename)
			if os.path.isdir(subitem):
				print("%s size = %i o" % (directory, (dir_size(directory))))
				tree(subitem, indentation + '  ')
	except OSError:
		pass

def main():
	'''Main Program'''
	try:
		starting_path = sys.argv[1]
	except IndexError:
		starting_path = raw_input("Path: ")
	tree(starting_path, '')
	return 0

if __name__ == '__main__':
	main()
