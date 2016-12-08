import matplotlib.pyplot as plt
import random

def binary_search(target, epsilon):
    guess = 1.0
    bottom = 1.0
    top = float("inf")
    steps = 0

    while abs(target-guess)>epsilon:
        steps += 1
        if guess < target:
            bottom = guess
            guess = min((top+bottom)/2, guess*2)
        elif guess > target:
            top = guess
            guess = max((top+bottom)/2, guess*.75)
        #print("top:{} bottom:{} guess:{}".format(top, bottom, guess))
    return guess, steps

target = []
steps_to_find = []

for _ in xrange(1000):
    t = random.randint(1,1e10)
    steps = binary_search(t, t/100)[1]
    target.append(t)
    steps_to_find.append(steps)

plt.scatter(target, steps_to_find)
plt.show()
