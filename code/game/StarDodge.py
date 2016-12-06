import os, sys
import pygame
from pygame.locals import *
import random
import time

pygame.init()
screen = pygame.display.set_mode((320, 640))
pygame.display.set_caption('Mouse Dodge')
pygame.mouse.set_visible(0)

background = pygame.image.load('rec/bg.png')
game_over = pygame.image.load('rec/game_over.png')
explosion = pygame.image.load('rec/explosion.png')
mouse_pos = pygame.mouse.get_pos()

class Game():
    def __init__(self):
        # get player
        self.player = pygame.image.load('rec/mouse.png')
        self.player_r = self.player.get_bounding_rect()
        #load images and rects for the comets
        self.load_img()
        #Pygame clock
        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        #Variables
        
        self.state = 1
        self.money = 0
        self.str_spd1 = 6
        self.str_spd2 = 5
        self.str_spd3 = 7
        self.laser = True
        while 1:
            self.Loop()
            
    def load_img(self):
        self.star = pygame.image.load('rec/star.png')
        self.star_r = self.star.get_bounding_rect()
        self.ran_x = random.randint(20,300)
        self.star2 = pygame.image.load('rec/star2.png')
        self.star2_r = self.star2.get_bounding_rect()
        self.ran_x2 = random.randint(20,300)
        self.star3 = pygame.image.load('rec/star3.png')
        self.star3_r = self.star3.get_bounding_rect()
        self.ran_x3 = random.randint(20,300)
        self.laser_img = pygame.image.load('rec/laser.png')
        self.laser_img_r = self.laser_img.get_bounding_rect()
        
        
        
    def update(self):
        #get mouse coords
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_x, self.mouse_y = self.mouse_pos

        (self.player_r.x, self.player_r.y) = self.mouse_pos
        #Set random x coord
        self.star_r.x = self.ran_x
        self.star2_r.x = self.ran_x2
        self.star3_r.x = self.ran_x3
        # set Comet speeds
        self.star_r.y += self.str_spd1
        self.star2_r.y += self.str_spd2
        self.star3_r.y += self.str_spd3
        
        if self.star_r.y > 640:
            self.star_r.y = 0
            self.ran_x = random.randint(5,110)
            
        if self.star2_r.y > 640:
            self.star2_r.y = 0
            self.ran_x2 = random.randint(100,200)
            
        if self.star3_r.y > 640:
            self.star3_r.y = 0
            self.ran_x3 = random.randint(190,315)
            
        self.laser_img_r.y = self.mouse_y
        self.laser_img_r.y -= 3
        
    def blitPlayer(self, screen):
        screen.blit(self.player,(self.mouse_pos))
        screen.blit(self.star,(self.ran_x, self.star_r.y))
        screen.blit(self.star2,(self.ran_x2, self.star2_r.y))
        screen.blit(self.star3,(self.ran_x3, self.star3_r.y))

        if self.laser == True and pygame.mouse.get_pressed()[1]:
            screen.blit(self.laser_img,(self.mouse_x, self.laser_img_r.y))
        
        if self.player_r.colliderect(self.star_r)or self.player_r.colliderect(self.star2_r)or self.player_r.colliderect(self.star3_r):
            self.state = 0
            
            
    def main_menu(self):
        
        self.main = pygame.image.load('rec/main.png')
        screen.blit(self.main,(0,0))
        self.play = pygame.image.load('rec/play.png')
        self.play_r = self.play.get_bounding_rect()
        self.play_r.x,self.play_r.y = (100,400)
        screen.blit(self.play,(100, 400))
        screen.blit(self.player,(self.mouse_pos))
        if self.player_r.colliderect(self.play_r)and pygame.mouse.get_pressed()[0]:
            self.state = 2

    def store(self):
        self.store = pygame.image.load('rec/store.png')
        screen.blit(self.store,(0,0))
        laser_item = pygame.image.load('rec/laser_item.png')
        self.lsr_itm_r = self.play.get_bounding_rect()
        if self.player_r.colliderect(self.lsr_itm_r)and pygame.mouse.get_pressed()[0]:
            self.laser = True
        
        
        
            
    def game_over(self):
        key = pygame.key.get_pressed()
        screen.blit(game_over,(0,0))
        if key[pygame.K_RETURN]:
            self.state = 1
    def Tick(self):
        # updates to player location and animation frame
        self.clock.tick()
        
        
    def eventLoop(self):
        # the main event loop, detects keypresses
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            
    def Loop(self):
        # main game loop
        self.eventLoop()
        self.update()
        if self.state == 0:
            self.game_over()
        if self.state == 1:
            self.main_menu()
        if self.state == 2:
            if pygame.time.get_ticks() - self.last_tick > 40:
                self.Tick()
                self.Draw()
        if self.state == 4:
            self.store()
        pygame.display.update()

    def Draw(self):
        screen.blit(background,(0,0))
        self.blitPlayer(screen)
        

Game()
