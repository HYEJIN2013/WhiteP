from random import randint
from mage import Mage
from monster import Monster

#work in progress 
class TestFight():

	def robotPlayer(self):
		robotClass = str((randint(1,2)))
		if robotClass == str(1):
			roboClass = Mage()
			print("Computer:")
			roboClass.robotAttack()
		elif robotClass == str(2):
			roboClass = Monster()
			print("Computer:")
			roboClass.robotAttack()
	
	def onePlayer(self):
		playerOne = (input("Which class would you like to play? Press 1 for a Mage, 2 for a Monster or 3 to hear about both classes!"))
		if playerOne == str(1):
			playClass = Mage()
			self.robotPlayer()
			print("Player 1:")
			playClass.humanAttack()
		elif playerOne == str(2):
			playClass = Monster()
			self.robotPlayer()
			print("Player 1:")
			playClass.humanAttack()
		elif playerOne == str(3):
			print("The Mage is has higher health but his attacks are more random in damage.")
			print("The Monster has lower health, but his attacks are consistant.")
			self.onePlayer()
		else:
			self.onePlayer()

	def begin(self):
		print("Hello and welcome!")
		print("To start will it be one player and a computer, or two players?")
		answer = str (input("Type 1 for one player, 2 for two players!"))
		if answer == str(1):
			self.onePlayer()


test = TestFight()
test.begin()
