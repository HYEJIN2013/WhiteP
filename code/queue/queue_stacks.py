# Works in Python 2 and Python 3
# Author: Marcos Castro - 30/03/2015
# Goal: to implement a queue with two stacks


stack1, stack2 = [], [] # my stacks


def enqueue(x): # inserts the element in the stack1
	stack1.append(x)


def dequeue(): # removes a element

	if not stack2: # if stack2 is empty 
		while stack1: # while stack1 is not empty
			# removes the last element of stack1 and inserts in stack2
			stack2.append(stack1.pop())

	return stack2.pop() # returns the last element of stack2


if __name__ == "__main__":

	# inserts elements...
	enqueue(5)
	enqueue(10)
	enqueue(15)
	enqueue(20)

	# shows the two first elements...
	print(dequeue())
	print(dequeue())
