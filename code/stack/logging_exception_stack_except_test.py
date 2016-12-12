#!/usr/bin/env python
#coding=utf8

##########################################################################################
from class_test import A, B
from except_log import log_exception

##########################################################################################
def main_1():
	a = A()
	try:
		print a.m0()
		print a.m1(3,0)
	except Exception as e:
		log_exception()
		print "main_1:Error <%s>" % str(e)

##########################################################################################
def main_2():
	a = A()
	b = B()
	try:
		print b.m0()
		print b.m1(3,a.m0())
	except Exception as e:
		log_exception()
		print "main_2:Error <%s>" % str(e)

##########################################################################################
def main():
	try:
		main_1()
		main_2()
	except Exception as e:
		print "main:Error <%s>" % str(e)

##########################################################################################
if __name__ == '__main__':
	main()
