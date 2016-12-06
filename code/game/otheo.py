#othelo

import random
import sys

def drawBoard(board):
    # This function prints out the board that it was passed. Returns None.
    HLINE = '  +---+---+---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |   |   |'

    print('    1   2   3   4   5   6   7   8')
    print(HLINE)
    for y in range(8):
        print(VLINE)
        print(y+1, end=' ')
        for x in range(8):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(VLINE)
        print(HLINE)


def resetBoard (board):
    #resets the boards for start of game

    for x in range (8):
        for y in range (8):
            board [x] [y] = ' '


    #starting pieces
    board [3] [3] = 'X'
    board [4] [4] = 'X'
    board [3] [4] = 'O'
    board [4] [3] = 'O'

def getNewBoard ():
    # creates a brand new, blank board data structure
    board = []
    for i in range(8):
        board.append(['  '] * 8)

    return board

def isValidMove (board, tile, xstart, ystart):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.

    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []

    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:

        x,y = xstart, ystart
        x += xdirection #first step in the direction
        y += ydirection # first step in the direction
        if not isOnBoard (x,y):
            continue

        while board [x] [y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard (x,y): # break out of while loop and back into for loop
                break

        if not isOnBoard(x,y):
            continue

        if board [x] [y] == tile:
            # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
            while True:
                x -= xdirection
                y -= ydirection
                if x == xstart and y == ystart:
                    break
                tilesToFlip.append([x,y])
    
        board [xstart] [ystart] = ' ' #restores the empty space
        if len(tilesToFlip) == 0: #if no tiles were flipped this is not a valid move
            return False
        return tilesToFlip




def isOnBoard (x,y):
    #returns true is the coorinates are located on the board
    return x >= 0 and x <= 7 and y >= 0 and y <=7

def getBoardWithValidMoves (board, tile):
    #returns a new board with . marking the valid moves the given player can make
    dupeBoard = getBoardCopy (board) 
    
    for x,y in getValidMoves (dupeBoard, tile):
        dupeBoard[x] [y] = '.'
    return dupeBoard

def getValidMoves (board, tile):
    #returns a list of valid moves
    validMoves =[]

    for x in range (8):
        for y in range(8):
            if isValidMove (board, tile,x,y) != False:
                validMoves.append ([x,y])
    return validMoves

def getScoreOfBoard (board):
    #determine score by counting tiles. returns a diconary with keys 'X' and 'O'
    xscore = 0
    oscore = 0

    for x in range(8):
        for y in range(8):
            if board [x] [y] == 'X':
                xscore += 1
            if board [x] [y] == 'O':
                oscore += 1
    return {'X': xscore, 'O' :oscore}

def enterPlayerTile():
    #lets the player type with tile they want to be
    #returns a list with the player first and the computer second
    tile = ''
    while not (tile == 'X' or tile == "O"):
        print ('Do you want to be X or O?')
        tile = input().upper()

    if tile == 'X':
        return ['X','O']
    else:
        return ['O','X']


def whoGoesFirst (tile):
    if tile == 'X':
        return 'player'
    else:
        return 'computer'

def playAgain ():
    print ('do you want to play again? (yes/no)')
    return input().lower().startswith('y')

def makeMove (board,tile,xstart,ystart):
        #place the tile on the board at xstart, ystart and flips any of the oppents pieces
        # returns False if it is invalid, true if it is valid

        tilesToFlip = isValidMove(board,tile,xstart,ystart)

        if tilesToFlip == False:
            return False

        board [xstart] [ystart] = tile
        for x,y in tilesToFlip:
            board [x] [y] = tile
        return True

def getBoardCopy(board):
    # Make a duplicate of the board list and return the duplicate.
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]

    return dupeBoard


def isOnCorner (x,y):
    # Returns True if the position is in one of the corners
    return (x==0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

def getPlayerMove (board, playerTile):
    # Let the player type in their move
    # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')

    DIGITS = '1 2 3 4 5 6 7 8'.split ()

    while True:
        print('Enter you move, or type quit to end the game, or hints to turn them on or off.')
        move = input().lower()

        if move == 'quit':
            return 'quit'
        if move == 'hints':
            return 'hints'

        if len(move) == 2 and move[0] in DIGITS and move[1] in DIGITS:
            
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                print ('Not Valid Move')
                continue
            else:
                
                break
        
        else:
            print ('That is not a valid move. Type the X digit (1-8), then the Y digit (1-8)')
            print ('For example, 81 will be the top-right corner')
            
    return [x,y]

def getComputerMove (board, computerTile):
    # the computer will determine the best move and return that move as a [x,y] list

    possibleMoves = getValidMoves (board, computerTile)

    
    for x,y in possibleMoves:
        #always go for the corners
        if isOnCorner (x,y):
            return [x,y]

    #goes though all possible moves and rembers the best one
    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove (dupeBoard, computerTile, x,y)
        score = getScoreOfBoard (dupeBoard) [computerTile]
        if score > bestScore:
            bestMove = [x,y]
            bestScore = score

    return bestMove


def showPoints(playerTile, computerTile):
    #Prints out the game board
    scores = getScoreOfBoard (mainBoard)
    print ('you have %s points. The computer has %s points' % (scores[playerTile], scores[computerTile]))


print ('Welcome to Othelo')

while True:
    # reset the game and the board
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile ()
    showHints = False
    turn = whoGoesFirst(playerTile)
    print('The ' + turn + ' will go first.')

    while True:

        if turn == 'player':
            #players turn
            if showHints:
                validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                drawBoard (validMovesBoard)
            else:
                drawBoard(mainBoard)

            showPoints(playerTile, computerTile)
            move = getPlayerMove (mainBoard, playerTile)

            if move == 'quit':
                print ('Thanks for playing')
                sys.exit () #terminate the game
            elif move == 'hints':
                continue
            else:
                makeMove (mainBoard, playerTile, move[0], move[1])


            if getValidMoves (mainBoard, computerTile) == []:
                break
            else:
                turn = 'computer'

        else:
            # computer's turn
            drawBoard (mainBoard)
            showPoints(playerTile, computerTile)
            input ("Press enter to see the computer's move.")

            x, y = getComputerMove (mainBoard, computerTile)
            makeMove (mainBoard, computerTile, x,y)

            if getValidMoves (mainBoard, playerTile) == []:
                break
            else:
                turn = 'player'
    
    # display final score
    drawBoard (mainBoard)
    scores = getScoreOfBoard(mainBoard)

    print ('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))
    if scores [playerTile] > scores[computerTile]:
        print ('You Won')
    elif scores [computerTile] > scores[playerTile]:
        print ('You lost')
    else:
        print('The game was a tie')

    if not playAgain ():
        break
    
