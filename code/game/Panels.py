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
