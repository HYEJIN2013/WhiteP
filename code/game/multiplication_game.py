import random
import time

digit = int(input("Enter digit: "))
if digit <= 0:
    print("digit must more than zero")

min = (10**(digit - 1)) - 1
max = 10**digit

while True:
    a = random.randrange(min, max)
    b = random.randrange(min, max)

    expression = str(a) + " x " + str(b) + " = "
    start = time.clock()
    ans = input(expression)
    correct = a * b
    if correct == int(ans):
        print("Correct")
    else:
        print("Wrong, Answer: ", correct)

    print("Time: ", time.clock() - start)
    print("")
