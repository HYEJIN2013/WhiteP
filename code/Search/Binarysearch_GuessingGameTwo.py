def printanswer(answer, guess, count):
    print("My guess is: %d"%guess)
    if answer > guess:
        print("Too low")
        return 0
    elif answer < guess:
        print("Too high")
        return 1
    elif answer == guess:
        print("I have got it!!!!")
        print("I guessed total %d times" % count)
        return 2

def startgame():
    count = 1
    goal = int(input("Please input your answer number (0-100) "))
    start = 0
    end = 100
    while True:
        middle = round((end + start) / 2)
        guess = middle
        a = printanswer(goal,guess,count)
        if a == 2:
            break
        elif a == 0:
            start = middle
            count += 1
        elif a == 1:
            end = middle
            count += 1
