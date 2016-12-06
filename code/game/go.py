#import sys
import pygame
from pygame import *
import main
from main import *

win_width = 800
win_height = 600
win_wh = (win_width, win_height)
bgc = "#000000"
timer = pygame.time.Clock()
coord = (0, 0)
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode(win_wh)




def main():

    bg = Surface(win_wh)
    bg.fill(Color(bgc))
    new_hero = main.new_hero()
    heros = main.heroes()
    mouse = False
    entities = pygame.sprite.Group()
    blocks = []
    heros.add(new_hero.create(0, (30, 30)), entities, blocks)

    while 1:
        timer.tick(60)
# EVENTS EVENTS  EVENTS  EVENTS  EVENTS  EVENTS  EVENTS  EVENTS  EVENTS  EVENTS  EVENTS  EVENTS

        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit, "QUIT"
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit
            if e.type == MOUSEBUTTONDOWN:
                mouse = True
            if e.type == MOUSEBUTTONUP:
                mouse = False
            if e.type == KEYDOWN and e.key == K_F1:
                heros.add(new_hero.create(1, (40, 40)), entities, blocks)
            if e.type == KEYDOWN and e.key == K_F2:
                heros.add(new_hero.create(2, (50, 50)), entities, blocks)
            if e.type == KEYDOWN and e.key == K_r:
                main()

# LOGIC LOGIC LOGIC LOGIC LOGIC LOGIC LOGIC LOGIC LOGIC LOGIC LOGIC LOGIC LOGIC LOGIC LOGIC LOGIC

# GRAPHIC GRAPHIC GRAPHIC GRAPHIC GRAPHIC GRAPHIC GRAPHIC GRAPHIC GRAPHIC GRAPHIC GRAPHIC GRAPHIC

        screen.blit(bg, (0, 0))
        clock.tick(60)
        coord = (win_width/2, win_height/2)
        heros.update(mouse, blocks, coord)
        for en in entities:
            screen.blit(en.image)
        fontimg = font.render(str(clock.get_fps()), 0, (0, 0, 0))
        screen.blit(fontimg, (0, 0))
        pygame.display.update()




if __name__ == "__main__":
    main()
