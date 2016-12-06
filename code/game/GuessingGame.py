import random, sys

#function to compare the generated number with the user's guess
def compareNums(user_guess, number):
    while number != user_guess:
       if user_guess < number:
            print('Your guess is too low...')
            #get a new guess
            user_guess = getGuess()
       elif user_guess > number:
            print('Your guess is too high...')
            #get a new guess
            user_guess = getGuess()
       else:
           return number

#Function to retrieve user input
def getGuess():
    guess = 0
    while guess < 1 or guess > 9:
        guess = input('Guess a number between 1 and 9:')
        #Make sure the input is an integer
        try:
           guess = int(guess)
        except ValueError:
           print("That's not an integer!")
           guess = 0
        if guess == 0:
            pass
        #make sure the number is between 1 and 9 (inclusive)
        elif guess > 9 or guess < 1:
            print('That number is not within my range!')
            guess = 0
        else:
            return int(guess)

#Function to quit or play again
def playAgain():
    choice = ''
    while choice != 'Y' or choice != 'y' or choice != 'N' or choice != 'n':
        choice = input('Would you like to play again? (Y/N)')
        #Make sure the choice is a letter
        try:
            choice = str(choice)
        except ValueError:
            choice = ''
        if choice == 'Y' or choice == 'y':
            break
        elif choice == 'N' or choice == 'n':
            sys.exit()
        else:
            print('Invalid Entry')

while True:
    number = random.randint(1, 9)
    user_guess = getGuess()
    compareNums(user_guess, number)
    print('Congratulations! The number was', number)
    playAgain()

print(getGuess())
