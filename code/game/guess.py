import random

target = random.randint(1,20)
maxTries = 4
tries = 0 
guessed = False

while (tries <maxTries) and not guessed: 
    num = int (input('Guess A Number..'))
    if num == target:
        guessed = True
        print 'You guessed correctly.'
    else:
        if num < target:
            print 'Try Higher'
        else:
            print 'Try Lower'
    tries = tries + 1
    
if not guessed:
    print 'FAAAILED!!'
