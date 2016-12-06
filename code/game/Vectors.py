import math

class Vec2():
	def __init__(self, x = 0.0, y = 0.0):
		self.x = x
		self.y = y
	def __len__(self):
		return 2
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	def __ne__(self, other):
		return self.x != other.x or self.y != other.y
	def __add__(self, other):
		if type(other) == int or type(other) == float:
			return Vec2(self.x + other, self.y + other)
		return Vec2(self.x + other.x, self.y + other.y)
	def __sub__(self, other):
		if type(other) == int or type(other) == float:
			return Vec2(self.x - other, self.y - other)
		return Vec2(self.x - other.x, self.y - other.y)
	def __mul__(self, other):
		if type(other) == int or type(other) == float:
			return Vec2(self.x * other, self.y * other)
		return Vec2(self.x * other.x, self.y * other.y)
	def __div__(self, other):
		if type(other) == int or type(other) == float:
			return Vec2(self.x / other, self.y / other)
		return Vec2(self.x / other.x, self.y / other.y)
	def __mod__(self, other):
		if type(other) == int or type(other) == float:
			return Vec2(self.x % other, self.y % other)
		return Vec2(self.x % other.x, self.y % other.y)
	def __pow__(self, other):
		if type(other) == int or type(other) == float:
			return Vec2(self.x ** other, self.y ** other)
		return Vec2(self.x ** other.x, self.y ** other.y)
	def __neg__(self):
		self.x = -self.x
		self.y = -self.y
	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"
	def normalize(self):
		dist = math.sqrt(self.x ** 2 + self.y ** 2)
		if dist != 0:
			self.x /= dist
			self.y /= dist
	def getNormalized(self):
		dist = math.sqrt(self.x ** 2 + self.y ** 2)
		if dist != 0:
			return Vec2(self.x / dist, self.y / dist)
	def getAbs(self):
		return Vec2(abs(self.x), abs(self.y))
	def getDist(self):
		return math.sqrt(self.x ** 2 + self.y ** 2)
