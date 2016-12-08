#!/usr/bin/env python

import json
import random
import time

# replace Queue.Queue with multiprocessing.Queue
from multiprocessing import Process, Queue

def random_message():
	"""create a dict of junk data, return as json"""

	msg = {}

	for i in range(9):
		msg[random.random()] = random.random()

	return json.dumps(msg)

def fill_queue(q):

	print 'started create'

	for i in range(500):
		msg = random_message()
		q.put(msg)
		print 'put.'
		time.sleep(0.01)
	

def read_queue(q):

	print 'started read'
	for i in range(5000):
		print 'got. %s' % q.get()

if __name__ == '__main__':

	q = Queue()

	write = Process(target=fill_queue, args=(q,))
	read = Process(target=read_queue, args=(q,))

	write.start()
	read.start()
