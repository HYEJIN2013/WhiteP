import math

class SegmentTree:
	def __init__(self, array):
		self.n = (1 << int(math.log(len(array) - 1, 2) + 1))
		self.tree = array + [10 ** 9] * (2 * self.n - len(array))
		
		for i in range(self.n, 2 * self.n):
			self.tree[i] = self.tree[i - self.n]

		for i in range(self.n - 1, 0, -1):
			self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])

	def find_min(self, left, right):
		ans = 10 ** 9
		left += (self.n - 1)
		right += (self.n - 1)
		while left <= right:
			if left & 1:
				ans = min(ans, self.tree[left])
			if not (right & 1):
				ans = min(ans, self.tree[right])
			left = (left + 1) // 2
			right = (right - 1) // 2
		return ans

	def update(self, i, x):
		i += (self.n - 1)
		self.tree[i] = x
		i //= 2
		while i:
			self.tree[i] = min(self.tree[2 * i], self.tree[2 * i + 1])
			i //= 2
