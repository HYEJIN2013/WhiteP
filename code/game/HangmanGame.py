import random
import string

WORDLIST_FILENAME = "C:/Users/rvargas/words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

    
def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------


def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE...
    new = ""
    for i in secretWord:
        if i in lettersGuessed:
            new += i
            if new == secretWord:
                return True
        else:
            return False


def getGuessedWord(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that represents
      what letters in secretWord have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE...
    result = list(secretWord)
    for i in result:
        if i not in lettersGuessed:
            result[result.index(i)] = " _ "
    transtring = ''.join(result)
    return transtring


def getAvailableLetters(lettersGuessed):
    '''
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE...
    Alletters = string.ascii_lowercase
    result = list(Alletters)
    for i in lettersGuessed:
        if i in result:
            result.remove(i)
    transtring = ''.join(result)
    return transtring

def hangman(secretWord):
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is {0:d} letters long".format(len(secretWord)))
    gameOver = False
    guessesLeft = 8
    lettersGuessed = []
    while not gameOver:
        print("-" * 11)
        print("You have {0:d} guesses left".format(guessesLeft))
        availableLetters = getAvailableLetters(lettersGuessed)
        print("Available Letters: {0:s}".format(availableLetters))
        guess = raw_input("Please guess a letter: ")
        guess = guess[0].lower()
        if guess in availableLetters:
            lettersGuessed.append(guess)
            if guess in secretWord:
                response = "Good guess:"
                if isWordGuessed(secretWord, lettersGuessed):
                    gameOver = True
            else:
                guessesLeft -= 1
                response = "Oops! That letter is not in my word:"
                if guessesLeft == 0:
                    gameOver = True
        else:
            response = "Oops! You've already guessed that letter:"
        print("{0:s} {1:s}".format(response, getGuessedWord(secretWord, lettersGuessed)))
    print("-" * 11)
    if isWordGuessed(secretWord, lettersGuessed):
        print("Congratulations, you won!")
    else:
         print("Sorry, you ran out of guesses. The word was {0:s}.".format(secretWord))



def hangman(secretWord):
    '''
    secretWord: string, the secret word to guess.
    Starts up an interactive game of Hangman.
    * At the start of the game, let the user know how many 
      letters the secretWord contains.
    * Ask the user to supply one guess (i.e. letter) per round.
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computers word.
    * After each round, you should also display to the user the 
      partially guessed word so far, as well as letters that the 
      user has not yet guessed.
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE...
    print("Welcome to the Hangman game!")
    print('\n')
    print("My word has " + str(len(secretWord)) + " letters!")
    guesses = 8      # No. of guesses
    lettersGuessed = []   # Creating empty list
    Alletters = string.ascii_lowercase    # String containing all the lowercase letters
    while guesses > 0:    # Game starts
        print("You have " + str(guesses) + " guesses left!")
        print("Available letters: " + str(Alletters))
        letters = raw_input("Please guess a letter: ")
        if type(letters) != str:
            print("Invalid input! please enter one letter!")
        else:
            letterslower = letters.lower()     # Transfering input into lowercase
            #lettersGuessed = lettersGuessed.append(letterslower)  # Inserting inputs into a list
            lettersGuessed.append(letterslower)
            if letterslower not in Alletters:
                print("Opps! you have already guessed that letter: " + getGuessedWord(secretWord, lettersGuessed))
            else:
                if isWordGuessed(secretWord, lettersGuessed) == "True":
                    print("Congradualation! you won!")
                else:
                    print("Good guess: " + getGuessedWord(secretWord, lettersGuessed))
                    guesses -= 1
                    Alletters = getAvailableLetters(lettersGuessed)
    print("You have ran out of guess, the word is " + str(secretWord))
