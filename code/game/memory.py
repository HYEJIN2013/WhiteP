# implementation of card game - Memory
#Load in codeskulptor

import simplegui
import random

moves = 0
exposed = []
index = -1
state = 0
deck = range(8) + range(8)
random.shuffle(deck)
c1 = -1
c2 = -1

WIDTH = 50
HEIGHT = 100

# helper function to initialize globals
def new_game():
    global state, exposed, moves, deck
    state = 0 # no cards revealed
    random.shuffle(deck)
    moves = 0
    exposed = [False for i in range(16)]
    pass  

def mouseclick(pos):
    # add game state logic here
    global state, exposed, moves, c1, c2
    index = pos[0] // 50

    if not exposed[index]:

        if state == 0:
            exposed[index] = True
            c1 = index # record position of card
            state = 1 # 1 card revealed
            pass
        
        elif state == 1:
            exposed[index] = True
            c2 = index # record position of second card
            state = 2 # 2 cards revealed
            moves += 1 # increase moves
            
        elif state == 2:
            if not deck[c1] == deck[c2]:
                exposed[c1] = False # hide card1
                exposed[c2] = False # hide card2
            exposed[index] = True # reveal new card
            c1 = index # record position of new card
            c2 = -1 # reset c2
            state = 1 # one card revealed
    pass
        
def draw(canvas):
    global cards, WIDTH, HEIGHT  
    
    label.set_text("Turns = "+str(moves))
    
    for c in range(len(deck)):
        if exposed[c]:        
            canvas.draw_text(str(deck[c]), (WIDTH * c, HEIGHT - 20), 90, "white", 'serif')
        else:
            canvas.draw_polygon([(WIDTH * c, 0), (WIDTH * (c + 1), 0), (WIDTH * (c + 1), 100),(WIDTH * c, 100)], 3,"Black","Green");            
                           

                
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
