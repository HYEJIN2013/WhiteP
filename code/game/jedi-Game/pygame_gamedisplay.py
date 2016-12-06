import pygame
from pygame import Rect, Surface, font
import time
import threading
import os
STOPPED = 0
WALKING = 1

def in_bounds(position, size, bounds):
    return bounds[0][0] <= position[0] <= (bounds[1][0]-size[0]) \
           and bounds[0][1] <= position[1] <= (bounds[1][1]-size[1])

class JediAnimate():
    def __init__(self, image, xsize=240, ysize=240, numframes=5,
             numrows=5, *args, **kwargs):
        self.image = image
        self.step_num = 0
        self.xsize = xsize
        self.ysize = ysize
        self.xframe = xsize / numframes
        self.yframe = ysize / numrows
        self.numframes = numframes
        self.numrows = numrows

        animateThread = threading.Thread(target=self.update_state, args=args, kwargs=kwargs)
        animateThread.start()

    def image_rect(self):
        top = (self.step_num/int(self.numrows)) * self.yframe
        left = (self.step_num% int(self.numrows)) * self.xframe
        return (left,top), (self.xframe, self.yframe)

    def update_state(self):
        while True:
            time.sleep(.10)
            self.animate()

    def animate(self):
        self.step_num += 1
        self.step_num %= self.numrows * self.numframes


class JediCharacter(object):
    def __init__(self, image, position=[0,0], direction='right', xsize=128, ysize=192, numframes=4,
                 direction_map={'up': 3, 'down':0, 'left': 1, 'right': 2}, bounds=[[0,0],[400,400]], *args, **kwargs):
        self.image = image
        self.step_num = 0
        self.xsize = xsize
        self.ysize = ysize
        self.xframe = xsize/numframes
        self.yframe = ysize/len(direction_map)
        self.numframes = numframes
        self.position = position
        self.direction = direction
        self.moving = STOPPED
        self.direction_map = direction_map
        self.bounds=bounds
        self.weapon = None

        walkThread = threading.Thread(target=self.update_state, args=args, kwargs=kwargs)
        walkThread.start()

    def weapon_position(self):
        assert isinstance(self.weapon, JediAnimate)
        direction_offset = {'up': (0, -self.weapon.yframe),
                            'down': (0, self.yframe),
                            'left': (-self.weapon.xframe, 0),
                            'right': (self.xframe, 0)}

        return self.position[0] + direction_offset[self.direction][0], \
               self.position[1] + direction_offset[self.direction][1]


    def image_rect(self):
        top = self.direction_map[self.direction] * self.yframe
        left = self.step_num * self.xframe
        bottom = self.yframe
        right = self.xframe
        return (left,top),(right, bottom)

    def position(self):
        return self.position

    def update_state(self):
        while True:
            time.sleep(.25)
            if self.moving == WALKING:
                self.take_step()

    def take_step(self):
        self.step_num += 1
        self.step_num %= self.numframes
        direction_moves = {'up': (0, -self.ysize/10),
                           'down': (0, self.ysize/10),
                           'left': (-self.xsize/10, 0),
                           'right': (self.xsize/10, 0)}
        newPosition = [self.position[0] + direction_moves[self.direction][0],
                       self.position[1] + direction_moves[self.direction][1]]

        if in_bounds(newPosition, (self.xframe, self.yframe), self.bounds):
            self.position = newPosition
        else:
            self.moving = STOPPED

    def draw(self, screen):

        if self.weapon is not None:
            assert isinstance(self.weapon, JediAnimate)
            screen.blit(self.weapon.image, self.weapon_position(), Rect(self.weapon.image_rect()))

        screen.blit(self.image, self.position, Rect(self.image_rect()))

        #TODO: RENDER STATUS BAR

    def draw_status(self):
        pass
        # health
        # force_points


class GameDisplay():
    def __init__(self, caption="Jedi Battles"):
        pygame.init()
        pygame.font.init()

        width = 400
        height = 700  # lower 300 px for status

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.objects = []
        self.actions = []
        self.initGraphics()

    def update(self):
        #  60fps
        self.clock.tick(60)
        self.screen.fill(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        self.drawBoard()
        pygame.display.flip()

    def initGraphics(self):
        pass

    def drawBoard(self):
        for GUI_object in self.objects:
            GUI_object.draw(self.screen)

        self.process_actions()

    def process_actions(self):
        mouse = pygame.mouse.get_pos()
        click = False
        pygame.event.get()
        if pygame.mouse.get_pressed()[0]:
            click = True

        for action in self.actions:
            assert isinstance(action, Interaction_Object)
            if in_bounds(mouse, (1, 1), action.bounding_box()):
                action.mouse_over = True
                if click:
                    action.click()
            else:
                action.mouse_over = False
            action.draw(self.screen)


class Interaction_Object():
    def __init__(self, text, x, y, size_x, size_y, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.action = action

    def draw(self, screen):
        myfont = pygame.font.SysFont(None, 32)
        label = myfont.render(self.text, 1, (255, 255, 255))
        screen.blit(label, (self.x, self.y))

    def bounding_box(self):
        return [[self.x, self.y], [self.y + self.size_y, self.x + self.size_x]]

    def click(self):
        if self.action is not None:
            self.action()

class GamePlay():
    def __init__(self, *args, **kwargs):
        self.display = GameDisplay()
        self.characters = {}
        self.graphics = {}
        image_dir = os.path.join(os.path.abspath(os.path.curdir), 'images/characters')
        for dir, folders, files in os.walk(image_dir):
            for file in files:
                filename = os.path.join(dir, file)
                self.graphics[file] = pygame.image.load(filename).convert()
                self.characters[os.path.basename(file)[:-4]] = JediCharacter(self.graphics[file])

        self.attacks = {}
        image_dir = os.path.join(os.path.abspath(os.path.curdir), 'images/attacks')
        for dir, folders, files in os.walk(image_dir):
            for file in files:
                filename = os.path.join(dir, file)
                self.graphics[file] = pygame.image.load(filename).convert()
                self.attacks[os.path.basename(file)[:-4]] = JediAnimate(self.graphics[file])

        self.width = 400
        self.height = 400

        updateThread = threading.Thread(target=self.update, args=args, kwargs=kwargs)
        updateThread.start()

    def update(self):
        while True:
            self.display.update()

    def place_character(self, character, movement=None, direction=None, position=None):
        if movement is not None:
            character.moving = movement
        if direction is not None:
            character.direction = direction
        if position is not None:
            character.position = position
        self.display.objects.append(character)

    def enter_combat(self, character, direction):
        buffer = 30
        self.direction_box = {'up': {'box':[[0, (self.height+buffer)/2],
                                            [self.width, self.height]],    # bottom half
                                     'pos':[self.width/2, self.height-character.yframe]},    # middle of bottom

                              'down': {'box':[[0, 0],
                                              [self.width, (self.height-buffer)/2]],            # top half
                                     'pos':[self.width/2, 0]},                               # middle of top,

                              'left': {'box':[[(self.width + buffer)/2, 0],
                                              [self.width, self.height]],  # right half
                                     'pos':[self.height/2, self.width-character.xframe]},    # middle of right,

                              'right': {'box':[[0, 0],
                                               [(self.width-buffer)/2, self.height]], # left half
                                     'pos':[self.height/2, 0]},    # middle of bottom
                              }

        character.moving = WALKING
        character.direction = direction
        character.bounds = self.direction_box[direction]['box']
        character.position = self.direction_box[direction]['pos']
        self.place_character(character)

# def doCombat():
#     global game
#     game.enter_combat(game.characters['jedi'], 'down')
#     game.enter_combat(game.characters['anakin'], 'up')
#
# def anakinLightning():
#     global game
#     game.characters['anakin'].weapon = game.attacks['ForceLightning']

# game = GamePlay()
# actions = game.jedigame.actions
# actions.append(JediAction("Do combat!",0,0,200,50,doCombat))
# actions.append(JediAction("Give Lightning To Anakin!",0,50,200,50,anakinLightning))
