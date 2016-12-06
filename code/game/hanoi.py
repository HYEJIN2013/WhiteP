import time
import math
import random
from tkinter import *

random.seed(None)
COLOR = ['magenta', 'green', 'red', 'blue', 'orange', 'yellow', 'pink', 'purple', 'violet', 'white', 'cyan']
random.shuffle(COLOR)
SPEED = 0
ANI_FRAMES = 30
ANI_SPEED = 0

def binomial(i, n):
    return math.factorial(n) / (math.factorial(i) * math.factorial(n-i))

def bernstein(t, i, n):
    return binomial(i, n) * (t ** i) * ((1-t) ** (n-i))

def bezier(t, points):
    n = len(points) - 1
    x = y = 0
    for i, pos in enumerate(points):
        bern = bernstein(t, i, n)
        x += pos[0] * bern
        y += pos[1] * bern
    return x, y

def bezier_curve_range(n, points):
    for i in range(n):
        t = i / (n-1)
        yield bezier(t, points)


class Tower:
    def __init__(self, canvas, left, top, right, bottom):
        self.canvas = canvas
        self.discs = []
        self.valid_pos = 0

        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.width = self.right - self.left
        self.height = self.top - self.bottom
        self.center = self.left + self.width // 2

    def add(self, disc):
        self.discs.append(disc)
        self.valid_pos += 1

    def remove(self):
        del self.discs[-1]
        self.valid_pos -= 1

    def get_top(self):
        return self.discs[-1]

    def get_valid_pos(self):
        return self.valid_pos

    def reset(self):
        #底座
        self.canvas.create_line(self.left, self.bottom, self.right, self.bottom)
        #顶针
        self.canvas.create_line(self.center, self.bottom, self.center, self.top)

        for disc in self.discs:
            disc.reset()

    def move_to(self, target):
        #TODO:Animation
        disc = self.get_top()
        disc.update(target)

class Disc:
    def __init__(self, tk, canvas, level, owner):
        self.tk = tk
        self.canvas = canvas

        self.level = level
        self.owner = owner
        self.owner.add(self)
        self.height = 10
        self.pos = level
        self.id = 0
        self.color = COLOR[level % len(COLOR)]

        max_size = self.owner.width
        self.width = max_size - (self.level+1) * 10

    def update(self, owner):
        old_pos = self.pos
        self.pos = owner.get_valid_pos()

        old_left = self.owner.center - self.width // 2
        new_left = owner.center - self.width // 2
        old_top = self.owner.bottom - (old_pos - 1) * self.height
        new_top = owner.bottom - (self.pos - 1) * self.height

        #process data
        self.owner.remove()
        owner.add(self)
        self.owner = owner

        #Animation
        control1 = (old_left+50, old_top - 100)
        control2 = (new_left-50, new_top - 100)
        controlPoints = ((old_left, old_top), control1, control2, (new_left, new_top))

        for p in bezier_curve_range(ANI_FRAMES, controlPoints):
            self.canvas.move(self.id, p[0] - old_left, p[1] - old_top)
            self.tk.update()
            if (ANI_SPEED != 0):
                time.sleep(ANI_SPEED)
            old_left, old_top = p

    def reset(self):
        left = self.owner.center - self.width // 2
        right = self.owner.center + self.width // 2
        bottom = self.owner.bottom - self.pos * self.height
        top = bottom - self.height
        self.id = self.canvas.create_rectangle(left, top, right, bottom, fill=self.color)


def init():
    tk = Tk()
    tk.title("Hanoi Game")
    canvas = Canvas(tk, width=1000, height=800)
    canvas.pack()
    return tk, canvas

def Hanoi(tower1, tower2, tower3, level, tk):
    if level == 1:
        tower1.move_to(tower3)
        tk.update()
    else:
        Hanoi(tower1, tower3, tower2, level - 1, tk)
        if (SPEED != 0):
            time.sleep(SPEED)
        tower1.move_to(tower3)
        tk.update()
        if (SPEED != 0):
            time.sleep(SPEED)
        Hanoi(tower2, tower1, tower3, level - 1, tk)

def main(level):
    tk, canvas = init()
    tower1 = Tower(canvas, 50, 50, 250, 200)
    tower2 = Tower(canvas, 300, 50, 500, 200)
    tower3 = Tower(canvas, 550, 50, 750, 200)

    for i in range(level):
        disc = Disc(tk, canvas, i, tower1)
    tower2.reset()
    tower3.reset()
    tower1.reset()
    tk.update()
    time.sleep(2)

    Hanoi(tower1, tower2, tower3, level, tk)
    canvas.create_text(350, 250, text="Done!", font=("Arial", 50))

    return tk

import timeit
if __name__ == "__main__":
    level = input("Input the level:")
    tk = main(int(level))
    tk.mainloop()
