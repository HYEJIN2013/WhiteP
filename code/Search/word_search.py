from math import sqrt
import random
import sys

f = open(sys.argv[-1]).read() if sys.argv[-1].split('.')[-1] == 'txt' else open('chemicals.txt').read()
letter_scores = dict(zip('abcdefghijklmnopqrstuvwxyz', (1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 4, 2, 2, 4, 20, 2, 2, 2, 2, 4, 4, 8, 4, 10)))
score = lambda word: sum([letter_scores[letter] for letter in word])
words = sorted(f.split(), key=lambda word: (len(word), score(word)))

DENSITY = .57 # for some reason it shouldn't exceed 0.57
side_size = int(sqrt(len(f) / DENSITY)) + 1
board = [['.' for _ in xrange(side_size)] for _ in xrange(side_size)]

def can_i_add_word(word, board, x, y, vertical):
    for i in xrange(len(word)):
        if vertical:
            if board[y+i][x] not in ('.', word[i]):
                return False
        else:
            if board[y][x+i] not in ('.', word[i]):
                return False
    return True

def add_word(word, board):
    while True:
        x = random.randint(0, side_size-len(word))
        y = random.randint(0, side_size-len(word))
        vertical = random.random() > 0.5
        if can_i_add_word(word, board, x, y, vertical):
            for i in xrange(len(word)):
                if vertical:
                    board[y+i][x] = word[i]
                else:
                    board[y][x+i] = word[i]
            return

for word in words:
    add_word(word, board)

debug_mode = 'debug' in sys.argv

for i in xrange(side_size):
    for j in xrange(side_size):
        if board[i][j] == '.':
            board[i][j] = random.choice('abcdefghijklmnopqrstuvwxyz') if not debug_mode else ' '

print '\n'.join([' '.join(row) for row in board])
print
for word in words:
    print word
