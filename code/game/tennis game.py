#coding: utf-8
import random
import console
import speech
password = 'Bob123'
start = console.password_alert('enter the password: ')
#
def game():
	console.set_color(0.0,0.2,0.5)
	console.set_font('Times_New_Roman',15)
	purple = 0.5
	computer = random.randrange(1,4)
	volleys = 1
	player = int(raw_input('<1> forehand \n <2> backhand \n <3> lob \n <4> spike \n pick a swing: '))
	#swings and outputs
	while player and volleys < 25:
		console.set_color(0.5,0.3,purple)
		if player == 1 and computer == 2:
			speech.say('it\'s on the left')
		elif player == 1 and computer == 3:
			speech.say('it\'s up')
		elif player == 1 and computer == 4:
			speech.say('it\'s coming fast')
		if player == 2 and computer == 1:
			speech.say('he hit it back')
		elif player == 2 and computer == 3:
			speech.say('it\'s up again')
		elif player == 2 and computer == 4:
			speech.say('it\'s coming fast')
		if player == 3 and computer == 1:
			speech.say('it\'s flat and to the right')
		elif player == 3 and computer == 2:
			speech.say('it\'s flat and to the left')
		elif player == 3 and computer == 4:
			speech.say('it\‘s coming fast')
		if player == 4 and computer == 1:
			speech.say('he hit it back again')
		elif player == 4 and computer == 2:
			speech.say('it\'s faster and too the left')
		elif player == 4 and computer == 3:
			speech.say('it\'s up again')
		if player == computer:
			speech.say('he hit the net, you win')
			'he hit the net, you win \n'
			break
		player = int(raw_input('<1> forehand \n <2> backhand \n <3> lob \n <4> spike \n pick a swing: '))
		purple += 0.1
		volleys += 1
		computer = random.randrange(1,4)
	if volleys > 25:
		speech.say('you lose')
		print 'you took too long...you lose\n'
	else:
		speech.say('you won in ' + str(volleys) + ' volleys')
		print 'you won in ' + str(volleys) + ' volleys \n'
	#
	#play again?
	restart = int(raw_input('would you like to play again? \n 1 = yes? \n 2 = no?'))
	if restart == 1:
		console.clear()
		game()
	elif restart == 2:
		console.clear()
		speech.say('well then')
		print 'well then...😕'
#
if start == password:
	game()
else:
	while start != password:
		console.set_font('fontana', 20)
		speech.say('ERROR')
		print 'file corrupted...ERROR,ERROR,ERROR!!!!'
