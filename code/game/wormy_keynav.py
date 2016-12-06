import random, pygame, sys
from pygame.locals import *

FPS = 15
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
assert WINDOW_WIDTH % CELL_SIZE == 0, "Window width must be a multiple of cell size."
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Window height must be a multiple of cell size."
CELL_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

BLACK     = (  0,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Set a random starting point
    worm_x = random.randint(5, CELL_WIDTH - 6)
    worm_y = random.randint(5, CELL_HEIGHT - 6)
    direction = RIGHT

    while True:
        DISPLAYSURF.fill(BGCOLOR)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                ### TASK 1 - Set the direction based on the key pressed
                if event.key == K_LEFT:
                    direction = LEFT
                elif event.key == K_RIGHT:
                    pass
                elif event.key == K_UP:
                    direction = UP
                elif event.key == K_DOWN:
                    pass
                elif event.key == K_ESCAPE:
                    terminate()

        # move the worm in the direction it is moving
        if direction == UP and worm_y > 0:
            worm_y = worm_y - 1
        elif direction == DOWN and worm_y < (CELL_HEIGHT- 1):
            worm_y = worm_y + 1
        elif direction == LEFT and worm_x > 0:
            pass
        elif direction == RIGHT and worm_x < (CELL_WIDTH - 1):
            pass
                
        x = worm_x * CELL_SIZE
        y = worm_y * CELL_SIZE
        worm_segment_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, worm_segment_rect)
        worm_inner_segment_rect = pygame.Rect(x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, worm_inner_segment_rect)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
