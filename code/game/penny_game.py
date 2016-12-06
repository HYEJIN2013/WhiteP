import random

#*****************************************
#                                        *
#             Penny's game               *
#                                        *
# Sequences selected by the two players  *
player1 = [1,0,1,0]       
player2 = [0,1,0,0]
# iterations                             *
iterations = 1000000                     
#*****************************************

def game(arrayOne, arrayTwo):
  gameArray = []
  run = True
  loop = 0
  while run:
    loop += 1
    if len(gameArray) < 4:
      gameArray.append(toss())
    else:
      gameArray.append(toss())
      gameArray.pop(0)
    # Check if winner
    if len(gameArray) > 3:
      if arrayOne == gameArray:
        run = False
        return 1
      if arrayTwo == gameArray:
        run = False
        return 2

def toss():
  number = random.random()
  if number > 0.5:
    return 1
  else:
    return 0

numberOfPlays = 0
countWinner1 = 0
countWinner2 = 0
while numberOfPlays < iterations:
  numberOfPlays += 1
  winner = game(player1,player2)
  if winner == 2:
    countWinner2 +=1
  else:
    countWinner1 +=1

print 'Player 1 won: ' + str((float(countWinner1)/iterations)*100) + '%'
print 'Player 2 won: ' + str((float(countWinner2)/iterations)*100) + '%'
