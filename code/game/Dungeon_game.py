__author__ = 'John'

import random


CELLS = [(0,0),(0,1),(0,2),
         (1,0),(1,1),(1,2),
         (2,0),(2,1),(2,2)]

directions = {}

def set_initial_directions(directions_dict):

    for cell in CELLS:
        if cell != player:
            directions_dict.update({cell : 'NONE'})
        elif cell == player:
            directions_dict.update({cell : 'START'})

def get_direction(directions_dict,cell):
    if directions_dict[cell] == 'LEFT':
        return '<'
    elif directions_dict[cell] == "RIGHT":
        return '>'
    elif directions_dict[cell] == 'UP':
        return '^'
    elif directions_dict[cell] == 'DOWN':
        return 'v'
    else:
        return '_'

def set_direction(directions_dict,cell,direction):
    directions_dict[cell] = direction

def get_locations():
    monster = random.choice(CELLS)
    door = random.choice(CELLS)
    start = random.choice(CELLS)

    # if monster, door, or start are the same, do it again
    if monster == door or monster == start or door == start:
        return get_locations()

    return monster,door,start

def get_next_move(current_position,move):
    x, y = current_position

    if move == 'LEFT':
        y -= 1
    elif move == 'RIGHT':
        y += 1
    elif move == 'UP':
        x -= 1
    elif move == 'DOWN':
        x += 1

    return x,y

def moved_before(move,player):
    x, y = get_next_move(player,move)

    if directions[(x,y)] != 'NONE' and directions[(x,y)] != 'START':
        return True
    else:
        return False

def move_player(player,move):
    set_direction(directions,player,move)

    x,y = get_next_move(player,move)

    return x,y

def get_moves(player):
    moves = ['LEFT','RIGHT','UP','DOWN']
    #player = (x,y)

    if player[1] == 0:
        moves.remove('LEFT')
    if player[1] == 2:
        moves.remove('RIGHT')
    if player[0] == 0:
        moves.remove('UP')
    if player[0] == 2:
        moves.remove('DOWN')

    return moves

def draw_map(player):
    print(' _ _ _ ')
    tile = '|{}'

    for idx,cell in enumerate(CELLS):
        if idx in [0,1,3,4,6,7]:
            if cell == monster and monster == player:
                print(tile.format('D'),end="")
            elif cell == door and door == player:
                print(tile.format('E'),end="")
            elif cell == player:
                print(tile.format('X'),end ="")
            else:
                print(tile.format(get_direction(directions,cell)), end = "")
        else:
            if cell == monster and monster == player:
                print(tile.format('D|'))
            elif cell == door and door == player:
                print(tile.format('E|'))
            elif cell == player:
                print(tile.format('X|'))
            else:
                print(tile.format(get_direction(directions,cell)+ '|'))

def move_message(message,moves):
    print(message,end=" ")
    for i in range(0,len(moves)):
        if i != len(moves) - 1:
            print(moves[i],end=",")
        else:
            print(moves[i],end="")

    print('\nEnter QUIT to quit.')

monster, door, player = get_locations()

set_initial_directions(directions)

print('Welcome to the dungeon!')

while True:
    moves = get_moves(player)
    print("You're currently in room {}.".format(player)) #fill in with player position
    draw_map(player)
    move_message("You can move:" ,moves)

    move = input("> ")
    move = move.upper()

    if move == 'QUIT':
        break

    if move in moves:
        if not moved_before(move,player):
            player = move_player(player,move)
        else:
            print('You have moved here before, are you sure you wish to backtrack? y/n')
            choice = ""

            while choice.lower() != 'y' or choice.lower() != 'n':
                choice = input('> ')
                if choice == 'y':
                    player = move_player(player,move)
                    break
                elif choice == 'n':
                    move_message('Where do you wish to go then? Your available moves are:',moves)
                    newMove = input('> ')
                    newMove = newMove.upper()
                    if newMove == 'QUIT':
                        choice = newMove
                        break
                    player = move_player(player,newMove)
                    break
            if choice == 'QUIT':
                break


    else:
        print('** Walls are hard, stop walking into them! **')
        continue

    if player == door:
        draw_map(player)
        print("You escaped!")
        break
    elif player == monster:
        draw_map(player)
        print("You were eaten by the grue!")
        break
