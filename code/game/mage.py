from random import randint
class Mage():
	mageHealth = 1250
	mageStrength = 75

	def windSpell(self):
		wind = (randint(1,4))
		times = 0
		while wind <= 4:
			self.mageStrength
			print(self.mageStrength)
			wind = wind + 1
			times = times + 1
		print("It hits " + str(times) + " times")

	def fireSpell(self):
		fire = (randint(1,6))
		burn = 50
		if fire == 2:
			fireAttack = self.mageStrength*3
			print(fireAttack)
		if fire == 6:
			fireAttack = self.mageStrength*2
			burn = (randint(1,4)*burn)
			print(fireAttack + burn)
			print("Nice hit the enemy takes " + str(burn) + " burn damage!" )
		if fire != 2 and fire != 6:
			fireAttack = self.mageStrength*2
			print(fireAttack)

	def iceSpell(self):
		ice = (randint (1,3)*self.mageStrength)
		print(ice)

	def humanAttack(self):
		print("What attack do you wanna do?")
		player = str (input("Press 1 for a Wind Spell, 2 for a FireSpell or 3 for an Ice Spell!"))
		if player== str(1):
			self.windSpell()
		elif player== str(2):
			self.fireSpell()
		elif player== str(3):
			self.iceSpell()
		else:
			self.humanAttack()

	def robotAttack(self):
		robot = str((randint(1,3)))
		if robot == str(1):
			self.windSpell()
		elif robot == str(2):
			self.fireSpell()
		else:
			self.iceSpell()


	def alive(self):
		if self.mageHealth > 0:
			return True
		else:
			return False
