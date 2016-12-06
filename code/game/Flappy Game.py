from scene import *

from Vectors import *

from Panels import *

import sound

import math

import time

import random

class Flapper(Panel):
	def secondaryInit(self, velocity):
		self.velocity = velocity
	def doGravity(self, gravity):
		self.velocity += gravity
	def doTouch(self):
		self.velocity.y = 13.0 if self.velocity.y <= 0 else self.velocity.y + 7# = Vec2(0.0, 15.0)
	def doVelocity(self):
		self.x += self.velocity.x
		self.y += self.velocity.y
	def collideWithWall(self, wall):
		#wall should be a panel object
		#simple square collision
		return wall.isTouched(self.x, self.y) or wall.isTouched(self.x + self.w, self.y) or wall.isTouched(self.x, self.y + self.h) or wall.isTouched(self.x + self.w, self.y + self.h)
		
		

class MyScene (Scene):
	def genWall(self):
		#walls are 2 70 px thick panels and have a 200 px opening to go through
		#there should always be a 50 px gap between the ground and the wall opening
		#wall colors and alphas are pre-defined in the draw function so no need to set3 them here
		#use 2000 once the camera thing is set up
		#there is a 50x180 px goal piece in between the walls
		midstart = random.randint(50, self.bounds.h - 250)
		self.walls.append(Panel(self.flapper.x + self.bounds.w - 270, 0, 70, midstart, 0.0, 0.0, 0.0, 0.0))#bottom (?)
		self.walls.append(Panel(self.flapper.x + self.bounds.w - 270, midstart + 200, 70, self.bounds.h, 0.0, 0.0, 0.0, 0.0))#top (?)
		self.goals.append(Panel(self.flapper.x + self.bounds.w - 260, midstart + 10, 50, 180, 0.0, 0.0, 0.0, 0.0))
	def cullExcessWalls(self):
		wallsCopy = self.walls[:]
		for i in range(len(wallsCopy)):
			if wallsCopy[i].x < self.flapper.x - 1000:
				self.walls.pop(i)
	def setup(self):
		# This will be called before the first frame is drawn.
		self.flapper = Flapper(10.0, 300.0, 50, 50, 1.0, 0.0, 0.0, 1.0)
		self.flapper.secondaryInit(Vec2(6.0, 0.0))
		self.walls = []
		self.goals = []
		self.deathparticles = []
		self.ticks = 0
		self.points = 0
		self.deadtime = 0.0
		self.gamestate = "play"
		sound.load_effect('Jump')
		sound.load_effect('Clank')
	def draw(self):
		background(0.0, 0.0, 0.4)
		if (self.gamestate == "play"):
			#fill(self.flapper.r, self.flapper.g, self.flapper.b, self.flapper.a)
			#rect(300, self.flapper.y, self.flapper.w, self.flapper.h)
			image('_Image_4', 300, self.flapper.y, self.flapper.w, self.flapper.h)
			self.flapper.doGravity(Vec2(0.0, -.63))
			self.flapper.doVelocity()
			
			fill(0.0, 1.0, 0.0, 1.0)
			for i in self.walls:
				rect(i.x - self.flapper.x + 300, i.y, i.w, i.h)
			
			fill(0.8, 0.5, 0.0, 1.0)
			for i in self.goals:
				rect(i.x - self.flapper.x + 300, i.y, i.w, i.h)
			
			if (self.ticks % 100 == 0):
				self.genWall()
			self.cullExcessWalls()
			
			for i in self.goals:
				if (self.flapper.collideWithWall(i)):
					self.points += 1
					self.goals.pop(self.goals.index(i))
					break
			
			for i in self.walls:
				if (self.flapper.collideWithWall(i)):
					self.gamestate = "dead"
					sound.play_effect('Clank', 1.0)
					self.deadtime = time.time()
					for i in range(219):
						z = Flapper(300 + self.flapper.w / 2, self.flapper.y + self.flapper.h / 2, 7.0, 7.0, 1.0, 0.0, 0.0, 0.0)
						xdir = random.random() - .5
						ydir = random.random() - .5
						dist = math.sqrt(xdir ** 2 + ydir ** 2)
						if dist == 0:
							xdir = 0
							ydir = 0
						else:
							xdir /= dist
							ydir /= dist
						z.secondaryInit(Vec2(xdir, ydir) * random.randint(0, 20))
						self.deathparticles.append(z)
					break
			
			tint(1.0, 1.0, 1.0, 1.0)
			text("Points: " + str(self.points), "Arial", 20.0, 5.0, self.bounds.h - 25.0, 3)
			
			if (self.flapper.y < 0 or self.flapper.y + self.flapper.h > self.bounds.h + 20):
				self.gamestate = "dead"
				self.deadtime = time.time()
				sound.play_effect('Clank', 1.0)
				for i in range(219):
					z = Flapper(300 + self.flapper.w / 2, self.flapper.y + self.flapper.h / 2, 7.0, 7.0, 1.0, 0.0, 0.0, 0.0)
					xdir = random.random() - .5
					ydir = random.random() - .5
					dist = math.sqrt(xdir ** 2 + ydir ** 2)
					if dist == 0:
						xdir = 0
						ydir = 0
					else:
						xdir /= dist
						ydir /= dist
					z.secondaryInit(Vec2(xdir, ydir) * random.randint(0, 20))
					self.deathparticles.append(z)
			self.ticks += 1
		elif (self.gamestate == "dead"):
			#fill(self.flapper.r, self.flapper.g, self.flapper.b, self.flapper.a)
			#rect(300, self.flapper.y, self.flapper.w, self.flapper.h)
			
			fill(0.0, 1.0, 0.0, 1.0)
			for i in self.walls:
				rect(i.x - self.flapper.x + 300, i.y, i.w, i.h)
			fill(0.8, 0.5, 0.0, 1.0)
			for i in self.goals:
				rect(i.x - self.flapper.x + 300, i.y, i.w, i.h)
			fill(1.0, 0.0, 0.0, 1.0)
			for i in self.deathparticles:
				ellipse(i.x, i.y, i.w, i.h)
				i.doGravity(Vec2(0.0, -0.63))
				i.doVelocity()
			tint(1.0, 1.0, 1.0, 1.0)
			text("You Died", "Arial", 32.0, self.bounds.w / 2, self.bounds.h / 2 + 32, 5)
			text("Points: " + str(self.points), "Arial", 32.0, self.bounds.w / 2, self.bounds.h / 2 - 32, 5)
	def touch_began(self, touch):
		if (self.gamestate == "play"):
			self.flapper.doTouch()
			sound.play_effect('Jump', 1.0)
		elif (self.gamestate == "dead" and (self.deadtime + 1.0) < time.time()):
			self.setup()
	
	def touch_moved(self, touch):
		pass
		
	def touch_ended(self, touch):
		pass

run(MyScene())
Raw
 Panels.py
from scene import *

class Panel:
	def __init__(self, x, y, w, h, r, g, b, a):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.r = r
		self.g = g
		self.b = b
		self.a = a
		self.updates = 0
		self.shouldDestroy = False
	def isTouched(self, touchX, touchY):
		return self.x <= touchX <= self.x + self.w and self.y <= touchY <= self.y + self.h

class PanelBatch:
	def __init__(self):
		self.panels = []
		self.needsSort = False
	def doSort(self):#sorts panels by color
		if (self.needsSort):
			self.panels = sorted(self.panels, key=lambda o: -1 if (self.panels.index(o) == 0) else int(255 * o.a) << 3 + int(255 * o.r) << 2 + int(255 * o.g) << 1 + int(255 * o.b))
		self.needsSort = False
	def addPanel(self, panel):
		self.panels.append(panel)
		self.needsSort = True
	def extendPanels(self, panels):
		self.panels.extend(panels)
		self.needsSort = True
	def drawBatch(self):
		lastColor = (0, 0, 0, 0)
		fill(0, 0, 0, 0)
		for i in self.panels:
			if (lastColor != (i.r, i.g, i.b, i.a)):
				fill(i.r, i.g, i.b, i.a)
			rect(i.x, i.y, i.w, i.h)
