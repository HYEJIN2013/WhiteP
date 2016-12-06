# -*- coding: utf-8 -*-
from sys import exit
import random
import math
import shelve

my_p_name = ""
my_p_type = ""
my_p_level = 5
my_p_attack = ""
# FIRST ATTACK DAMAGE/HP FORMULA
my_p_max_attack_damage = my_p_level * 2
my_p_max_hp = (my_p_level * 5) + 20
my_p_hp = my_p_max_hp
my_p_exp = 0
# LEVEL UP FORMULA
exp_to_next_level = (my_p_level + 1) * 51

my_potions = 3
my_revives = 10
potion_value = int(math.ceil(my_p_max_hp / 2.0))
potion_used = False

this_name = ""
this_level = 1
this_max_attack_damage = 1
this_hp = 1
this_exp_value = 1
this_attack = ""

name = ""
badges = 0

started = False
chosen = False
battle_completed = False

instructions = "PUT INSTRUCTIONS HERE"
inspiration = "Let your story begin, and may your honesty and determination guide you towards success and happiness."
oak = "Professor Oak: "
trainer = "Trainer: "
brock = "Brock: "
misty = "Misty: "


# all locations must follow these naming rules:
# Full Town Name/Route + number, name of building or location(Home, Gym, Path), more specific as needed, _number 

def play(loc, dir):
	global started, chosen, name, badges
	global my_p_name, my_p_type, my_p_level, my_p_attack, my_p_max_attack_damage, my_p_hp, my_p_max_hp, exp_to_next_level, my_p_exp
	# these are all of the user options 
	def move(up_loc, down_loc):
		global started, chosen, name, badges, my_potions, potion_value, my_revives, my_p_name, my_p_type, my_p_level, my_p_attack, my_p_max_attack_damage, my_p_max_hp, my_p_hp, my_p_exp, exp_to_next_level
		
		text = raw_input("> ").lower()
		if text == "move up" or text == "up" or text == "^[[A":
			if up_loc == "none":
				print "You can't go any further up! Try again!"
				move(up_loc, down_loc)
			else:
				play(up_loc, "up")
		elif text == "move down" or text == "down" or text == "^[[B":
			if down_loc == "none":
				print "You can't go any further down! Try again!"
				move(up_loc, down_loc)
			else:
				play(down_loc, "down")
		elif text == "move":
			print "Where would you like to move?"
			where = raw_input("> ")
			if where == "up":
				play(up_loc, "up")
			elif where == "down":
				play(down_loc, "down")
			else:
				print "Hmmm... I'm not quite understanding you. Let's start over."
				play(loc, dir)
		elif text == "heal" or text == "pokecenter" or text == "pokécenter":
			if "city" in loc or "town" in loc:
				pokecenter()
				play(loc, dir)
			else:
				print "You'll have to move to a city or town to use a Pokécenter!"
				move(up_loc, down_loc)
		elif text == "potion":
			potion()
			move(up_loc, down_loc)
		elif text == "pokedex" or text == "pokédex" or text == "dex":
			print "~~ %s's %s ~~" % (name, my_p_name)
			print "Level: %d" % my_p_level
			print "Type: %s" % my_p_type
			print "Attack: %s" % my_p_attack
			print "Max Attack Damage: %d" % my_p_max_attack_damage
			print "HP: %d/%d" % (my_p_hp, my_p_max_hp)
			print "Total Exp.: %d" % my_p_exp
			print "Exp. to next level: %d" % exp_to_next_level
			print "~~ %s's %s ~~" % (name, my_p_name)
			stop = raw_input("... ")
			play(loc, dir)
		elif text == "info":
			print "~~ %s ~~" % name
			print "Badges: %d" % badges
			print "Revives: %d" % my_revives
			print "Potions:  %d" % my_potions
			print "Potion Value: %d" % potion_value
			stop = raw_input("... ")
			play(loc, dir)
		elif text == "mart" or text == "pokemart" or text == "pokémart":
			mart()
			play(loc, dir)
		elif text == "save":
			if "city" in loc or "town" in loc:	
				print "Are you sure you'd like to save your progress?"
				confirm = raw_input("> ").lower()
				
				if confirm == "yes":
					shelf_file = shelve.open('test_save')
					shelf_file['started_v'] = started
					shelf_file['chosen_v'] = chosen
					shelf_file['name_v'] = name
					shelf_file['badges_v'] = badges
					shelf_file['my_potions_v'] = my_potions
					shelf_file['potion_value_v'] = potion_value
					shelf_file['my_revives_v'] = my_revives
					shelf_file['my_p_name_v'] = my_p_name
					shelf_file['my_p_type_v'] = my_p_type
					shelf_file['my_p_level_v'] = my_p_level
					shelf_file['my_p_attack_v'] = my_p_attack
					shelf_file['my_p_max_attack_damage_v'] = my_p_max_attack_damage
					shelf_file['my_p_max_hp_v'] = my_p_max_hp
					shelf_file['my_p_hp_v'] = my_p_hp
					shelf_file['my_p_exp_v'] = my_p_exp
					shelf_file['exp_to_next_level_v'] = exp_to_next_level
					# not global variables
					shelf_file['location_v'] = loc
					shelf_file['direction_v'] = dir	
					shelf_file.close()
					
					print "Your game was successfully saved!"
					stop = raw_input("... ")
					play(loc, dir)
				else:
					print "Your game was not saved."
					play(loc, dir)
			else:
				print "You'll have to move to a city or town to save your game!"
				move(up_loc, down_loc)		
		elif text == "exit":
			print "Are you sure you want to exit the game?"
			print "Any unsaved progress will be lost."
			confirm = raw_input("> ").lower()
			if confirm == "yes" or confirm == "exit":
				print "Goodbye, %s!" % name
				exit()
			else:
				print "You have been returned to your game."
				move(up_loc, down_loc)
		elif text == "help":
			print instructions
			play(loc, dir)
		elif text == "gym" and loc == "pewter city":
			print "~~ Pewter City Gym ~~"
			print "Brock: Welcome %s!" % name
			stop = raw_input("... ")
			if badges == 0:
				print "I have heard of your strength."
				print "Are you ready to challenge me?"
				if raw_input("> ") == "yes":
					print "Okay, then let's get to it right away!"
					stop = raw_input("... ")
					print "~~ %s vs. Leader Brock ~~" % name
					gym("Brock", "Geodude")
					play(loc, dir)
				else:
					print "Come back when you are ready and we will battle."
					stop = raw_input("... ")
					play(loc, dir)
			elif badges == 1:
				print "How nice to see you, %s." % name
				print "I want to thank you."
				stop = raw_input("... ")
				print "Our battle has given me the inspiration to improve my skills and grow my Pokémon."
				stop = raw_input("... ")
				play(loc, dir)
			elif badges == 2:
				print "I see that you have earned the Cascade Badge, %s. Congratulations!" % name
				print "It was an honor to have had the chance to battle you."
				stop = raw_input("... ")
				play(loc, dir)
			else:
				print "Error: Badges > 2"
		elif text == "gym" and loc == "cerulean city":
			print "~~ Cerulean City Gym ~~"
			print misty + "Welcome %s!" % name
			stop = raw_input("... ")
			if badges == 0:
				print "You'll need to earn the Boulder Badge before you can challenge me!"
				stop = raw_input("... ")
				play(loc, dir)
			elif badges == 1:
				print "Wow, you are much cuter than I thought you'd be!"
				print "Are you ready to challenge me?"
				if raw_input("> ") == "yes":
					print "Okay, let's go for a swim!"
					stop = raw_input("... ")
					print "~~ %s vs. Leader Misty ~~" % name
					gym("Misty", "Staryu")
					play(loc, dir)
				else:
					print "Come back when you are ready and we will battle."
					stop = raw_input("... ")
					play(loc, dir)
			elif badges == 2:
				print "How nice to see you again!"
				print "I still get shivers thinking about how exciting our battle was!"
				stop = raw_input("... ")
				play(loc, dir)
			else:
				print "Error: Badges > 2"
		else:
			print "Hmmm... that doesn't sound like something you can do right now."
			move(up_loc, down_loc)
					
	# This is where everything happens
	if loc == "palet town home" and not started:
		print "~~ Welcome! ~~"
		stop = raw_input("... ")
		print "This is the quaint, quiet, and qualified Palet Town."
		stop = raw_input("... ")
		print "You have spent your dear childhood dreaming of Pokémon battles, gym badges, and so much more!"
		print "Today is the day on which all of your dreams will begin to become realities."
		stop = raw_input("... ")
		print "There is nothing left in your way. You are ready to persevere and build yourself into the greatest Pokémon trainor the world has ever seen."
		print "Once you step outside, the journey begins..."
		stop = raw_input("... ")
		
		started = True
		move("palet town path_1", "none")
	elif loc == "palet town home" and started:
		print "Mom: Hello %s! I hope that you and your Pokémon are healthy and happy!" % name
		stop = raw_input("... ")
		print "I know it can be a tough world out there, but you are working hard to figure it all out and find your unique place within it."
		stop = raw_input("... ")
		print "I’ll always be here for you. Stop by anytime you’d like!"
		move("palet town path_1", "none")
	elif loc == "palet town path_1":
		if not chosen:
			print "Ah isn't the air outside so wonderful?"
			print "Oh look! Just up ahead is Professor Oak's Lab! That is just where we need to go."
			move("palet town oak lab", "palet town home")
		else:
			print "Ah the precious air between the place you once called home and the place you first met %s." % my_p_name
			move("palet town oak lab", "palet town home")
	elif loc == "palet town oak lab" and chosen:
		print oak + "Well hello there, %s! How nice it is to see you!" % name
		stop = raw_input("... ")
		print "Your %s seems to be enjoying its time with you." % my_p_name
		print "You are taking excellent care of it, I am sure."
		stop = raw_input("... ")
		if badges == 0: 
			print "Keep moving up in this world to expand your love for Pokémon and achieve continuous challenge and growth!"
		elif badges == 1:
			print "I see you have received your first badge! How exciting!"
			print "Once you have both badges, come to me and I will give you your grand prize!"
		elif badges == 2:
			print "Congratulations on obtaining your second badge!"
			stop = raw_input("... ")
			print "Now that you have beaten both Brock and Misty, I can now bestow upon you the title of Pokémon Master."
			stop = raw_input("... ")
			print "You also receive a ticket to Ryan's Pokémon Version 2 ... whenever that happens..."
			stop = raw_input("... ")
			print "Feel free to keep training you %s, but that's it for now!" % my_p_name
		else:
			print "Error: Unexpected # of badges"
		move("palet town path_2", "palet town path_1")
	elif loc == "palet town oak lab" and not chosen:
		print oak + "Welcome %s!" % name
		stop = raw_input("... ")
		print "My name is Professor Oak, and I know everything there is to know about Pokémon!"
		stop = raw_input("... ")
		print "Congratulations on today being your 10th birthday, and thus the beginning of your Pokémon journey."
		stop = raw_input("... ")
		print "Now let's not waste any more time! You've come here to choose your very own Pokémon."
		stop = raw_input("... ")
		choose_starter()
		play("palet town path_2", "up")
	elif loc == "palet town path_2":
		print "Up ahead is the endless beauty that is the world of Pokémon."
		print "Down below is the serene comfort of home."
		move("route 1 path_1", "palet town oak lab")
	elif loc == "route 1 path_1":
		print "Alright, you are just outside of Palet Town to the south."
		print "Up ahead to the north is a large patch of grass."
		print "Beware of wild Pokémon in tall grass!"
		move("route 1 grass_1", "palet town path_2")
	elif loc == "route 1 grass_1":
		grass("route 1")
		print "The grass is very high, but you can spot the faint outline of Palet Town to the south."
		move("route 1 grass_2", "route 1 path_1")
	elif loc == "route 1 grass_2":
		grass("route 1")
		print "The grass is so high, you can't see anything!"
		move("route 1 grass_3", "route 1 grass_1")
	elif loc == "route 1 grass_3":
		grass("route 1")
		print "The grass is so high, you can't see anything!"
		move("route 1 grass_4", "route 1 grass_2")
	elif loc == "route 1 grass_4":
		grass("route 1")
		print "The grass is so high, you can't see anything!"
		move("route 1 grass_5", "route 1 grass_3")
	elif loc == "route 1 grass_5":
		grass("route 1")
		print "The grass is very high, but you can spot the faint outline of Veridian City to the north."
		move("route 1 path_2", "route 1 grass_4")
	elif loc == "route 1 path_2":
		print "Now you are on the southern outskirts of the historic and marvelous Veridian City."
		move("veridian city", "route 1 grass_5")
	elif loc == "veridian city":
		print "~~ Welcome to Veridian City! ~~"
		print "Verdian City is a small, but lively and pleasant city."
		print "You can visit the Pokécenter, or the Pokémart!"
		print "To the north is the vivid Veridian Forest, and to the south is Rt. 1 and Palet Town."
		move("veridian forest path_1", "route 1 path_2")
	elif loc == "veridian forest path_1":
		print "The Veridian Forest is up to the north. The trees are packed in thickly."
		print "To the south is Veridian City"
		move("veridian forest grass_1", "veridian city")
	elif loc == "veridian forest grass_1":
		grass("veridian forest")
		print "Just through the trees, to the south, you can see a short path to Veridian City."
		move("veridian forest grass_2", "veridian forest path_1")
	elif loc == "veridian forest grass_2":
		grass("veridian forest")
		print "The tress of the forest are very thick, making it very difficult to see."
		move("veridian forest grass_3", "veridian forest grass_1")
	elif loc == "veridian forest grass_3":
		grass("veridian forest")
		print "The tress of the forest are very thick, making it very difficult to see."
		move("veridian forest grass_4", "veridian forest grass_2")
	elif loc == "veridian forest grass_4":
		grass("veridian forest")
		print "The tress of the forest are very thick, making it very difficult to see."
		move("veridian forest grass_5", "veridian forest grass_3")
	elif loc == "veridian forest grass_5":
		grass("veridian forest")
		print "Just through the trees, you can see a grassy path to the north."
		move("veridian forest path_2", "veridian forest grass_4")
	elif loc == "veridian forest path_2":
		print "The Veridian Forest is down to the south. The trees are packed in thickly."
		print "To the north is a grassy path towards Pewter City. Watch out for more Pokémon!"
		move("route 2 grass_1", "veridian forest grass_5")
	elif loc == "route 2 grass_1":
		grass("route 2")
		print "The trees of the Veridian Forest can barely be seen to the south."
		move("route 2 grass_2", "route 2 path_1")
	elif loc == "route 2 grass_2":
		grass("route 2")
		print "The grass is so high, you can't see anything!"
		move("route 2 grass_3", "route 2 grass_1")
	elif loc == "route 2 grass_3":
		grass("route 2")
		print "Up ahead to the north, you can barely make out Pewter City."
		move("route 2 path_2", "route 2 grass_2")
	elif loc == "route 2 path_2":
		print "Just to the north is Pewter City."
		print "Down to the south is a grassy path towards the Veridian Forest."
		move("pewter city", "route 2 grass_3")
	elif loc == "pewter city":
		print "~~ Welcome to Pewter City! ~~"
		print "Pewter City is a secluded city located within the mountains."
		print "You can visit the Pokécenter, or the Pokémart!"
		print "You may also challenge the Gym Leader, Brock, if you feel you are ready."
		print "To the north is the formidable Mt. Moon, which leads to Cerulean City."
		print "To the south is the Veridian Forest leading to Veridian City."
		move("route 3 path_1", "route 2 path_2")
	elif loc == "route 3 path_1":
		print "Up ahead is a pretty patch a grass beneath a large mountain."
		print "Down below is the city of Pewter."
		move("route 3 grass_1", "pewter city")
	elif loc == "route 3 grass_1":
		grass("route 3")
		print "Doesn't the grass feel so soft beneath your feet?!"
		move("route 3 grass_2", "route 3 path_1")
	elif loc == "route 3 grass_2":
		grass("route 3")
		print "The grass is so high, you can't see anything!"
		move("route 3 grass_3", "route 3 grass_1")
	elif loc == "route 3 grass_3":
		grass("route 3")
		print "Up ahead is the towering Mt. Moon"
		move("route 3 path_2", "route 3 grass_2")
	elif loc == "route 3 path_2":
		print "You are at the southern foot of the towering Mt. Moon!"
		print "Few who enter can make it out unscathed!"
		move("mt moon_1", "route 3 grass_3")
	elif loc == "mt moon_1":
		grass("mt moon")
		print "The southern light only lights up a small area. Mt. Moon is a dark and scary place!"
		move("mt moon_2", "route 3 path_2")
	elif loc == "mt moon_2":
		grass("mt moon")
		print "It is very dark. You can only see a faint light to the south."
		move("mt moon_3", "mt moon_1")
	elif loc == "mt moon_3":
		grass("mt moon")
		print "It is so dark in here that you can't see anything!"
		move("mt moon_4", "mt moon_2")
	elif loc == "mt moon_4":
		grass("mt moon")
		print "It is so dark in here that you can't see anything!"
		move("mt moon_5", "mt moon_3")
	elif loc == "mt moon_5":
		grass("mt moon")
		print "It is so dark in here that you can't see anything!"
		move("mt moon_6", "mt moon_4")
	elif loc == "mt moon_6":
		grass("mt moon")
		print "It is very dark, but you can see a faint light to the north."
		move("mt moon_7", "mt moon_5")
	elif loc == "mt moon_7":
		grass("mt moon")
		print "The northern light only barely reveals the cave's entrance. Mt. Moon is an eery place to travel through!"
		move("route 4 path_1", "mt moon_6")
	elif loc == "route 4 path_1":
		print "You are at the northern foot of the towering Mt. Moon!"
		print "Few who enter make it out unscathed, but you've already proven your strength!"
		print "To the north, you can see the skyline of the great Cerulean City."
		move("route 4 grass_1", "mt moon_7")
	elif loc == "route 4 grass_1":
		grass("route 4")
		print "This grass is very luscious. You must be getting closer to some water."
		move("route 4 grass_2", "route 4 path_1")
	elif loc == "route 4 grass_2":
		grass("route 4")
		print "The grass is so high, you can't see anything!"
		move("route 4 grass_3", "route 4 grass_1")
	elif loc == "route 4 grass_3":
		grass("route 4")
		print "Ah, how beautiful Cerulean City looks through the edge of the grass."
		move("route 4 path_2", "route 4 grass_2")
	elif loc == "route 4 path_2":
		print "You are on the edge of the city."
		print "To the south is the path leading to the intimidating Mt. Moon."
		move("cerulean city", "route 4 grass_3")
	elif loc == "cerulean city":
		print "~~ Welcome to Cerulean City! ~~"
		print "Cerulean City is a booming city with tons of excitement."
		print "You can visit the Pokécenter, or the Pokémart!"
		print "You may also challenge the Gym Leader, Misty, if you feel you are ready."
		print "To the north is vast and endless ocean."
		print "To the south is the path to Pewter City, which goes through Mt. Moon."
		move("none", "route 4 path_2")
	else:
		"I don't know where we are!"

def ask_help():
	global my_revives, inspiration
	print "%s, would you like me to explain how to play before we start?" % name
	answer = raw_input("> ").lower()
	if answer == "yes":
		print "Excellent! Here is everything you need to know:"
		stop = raw_input("... ")
		print instructions
		stop = raw_input("... ")
		print "If you ever need help again, just type 'help'."
		stop = raw_input("... ")
		print inspiration
		stop = raw_input("... ")
		
	elif answer == "no":
		print "Great!"
		print "If you ever need help, just type 'help'."
		stop = raw_input("... ")
		print inspiration
		stop = raw_input("... ")
	elif answer == "no thank you":
		my_revives += 1
		print "How polite! I just gave you an extra revive!"
		print "You don't even know what those are yet!"
		stop = raw_input("... ")
		print "Anyways... if you ever need help, just type 'help'." 
		stop = raw_input("... ")
		print inspiration
		stop = raw_input("... ")
	else:
		print "Hmmm... I didn't quite understand your answer. I'll try again." 
		ask_help()
def start():
	global started, chosen, name, badges, my_potions, potion_value, my_revives, my_p_name, my_p_type, my_p_level, my_p_attack,my_p_max_attack_damage, my_p_hp, my_p_max_hp, my_p_exp, exp_to_next_level
	
	print "~~~ Pokémon Game ~~~"
	print "New Game --- Continue"
	choice = raw_input("> ").lower()
	if choice == "new game":
		print "Warning: If you save a new game, any previous data will be erase."
		stop = raw_input("... ")
		print "~~~ New Pokémon Game ~~~"
		print "Welcome to Palet Town! You've finally reached your 10th birthday, and you are ready to start your Pokémon journey!"
		stop = raw_input("... ")
		print "Before we get started, can you please tell me your name?"
		name_text = raw_input("> ")
		name = name_text
		print "Hello, %s!" % name
		stop = raw_input("... ")
		ask_help()
		play("palet town home", "up")	
	if choice == "continue":
		shelf_file = shelve.open('test_save')
		started = shelf_file['started_v']
		chosen = shelf_file['chosen_v']
		name = shelf_file['name_v']
		badges = shelf_file['badges_v']
		my_potions = shelf_file['my_potions_v']
		potion_value = shelf_file['potion_value_v']
		my_revives = shelf_file['my_revives_v']
		my_p_name = shelf_file['my_p_name_v']
		my_p_type = shelf_file['my_p_type_v']
		my_p_level = shelf_file['my_p_level_v']
		my_p_attack = shelf_file['my_p_attack_v']
		my_p_max_attack_damage = shelf_file['my_p_max_attack_damage_v']
		my_p_max_hp = shelf_file['my_p_max_hp_v']
		my_p_hp = shelf_file['my_p_hp_v']
		my_p_exp = shelf_file['my_p_exp_v']
		exp_to_next_level = shelf_file['exp_to_next_level_v']
		
		location = shelf_file['location_v']
		direction = shelf_file['direction_v']	
		shelf_file.close()
		
		print "~~~ %s's Pokémon Game ~~~" % name
		play(location, direction)
def level_up():
	global my_p_exp, my_p_level, exp_to_next_level, my_p_hp, my_p_max_hp, my_p_max_attack_damage, potion_value
					
	my_p_exp += this_exp_value
	exp_to_next_level -= this_exp_value
	print "Your %s gained %d exp." % (my_p_name, this_exp_value)
	if my_p_level < 100:
		if exp_to_next_level <= 0:
			before = my_p_max_hp
			
			# resetting all the variables after a level-up
			my_p_level += 1
			my_p_max_attack_damage = my_p_level * 2
			my_p_max_hp = (my_p_level * 5) + 20
			potion_value = int(math.ceil(my_p_max_hp / 2.0))
			
			diff = my_p_max_hp - before
			my_p_hp += diff
			stop = raw_input("... ")
			print "Congratulations, your %s grew to level %d!" % (my_p_name, my_p_level)
			stop = raw_input("... ")
					
			if exp_to_next_level < 0:
				leftover_exp = 0 - exp_to_next_level
			exp_to_next_level = ((my_p_level + 1) * 51) - leftover_exp
					
			evolve()
		else:
			pass
					
		print "%s's total exp: %d" % (my_p_name, my_p_exp)
		print "Exp to next level: %d" % exp_to_next_level 
def evolve():
	global my_p_name, my_p_level
	if my_p_name == "Charmander":
		if my_p_level == 16:
			print "Congratulations, your Charmander has evolved into Charmeleon!"
			set_pokemon("Charmeleon", "Fire", "Flamethrower")
	elif my_p_name == "Charmeleon":
		if my_p_level == 36:
			print "Congratulations, your Charmeleon has evolved into Charizard!" 
			set_pokemon("Charizard", "Fire", "Fire Blast")
	elif my_p_name == "Bulbasaur":
		if my_p_level == 16:
			print "Congratulations, your Bulbasaur has evolved into Ivysaur!" 
			set_pokemon("Ivysaur", "Grass", "Razor Leaf")
	elif my_p_name == "Ivysaur":
		if my_p_level == 32:
			print "Congratulations, your Ivysaur has evolved into Venusaur!"
			set_pokemon("Venusaur", "Grass", "Solar Beam")
	elif my_p_name == "Squirtle":
		if my_p_level == 16:
			print "Congratulations, your Squirtle has evolved into Wartortle!"
			set_pokemon("Wartortle", "Water", "Skull Bash")
	elif my_p_name == "Wartortle":
		if my_p_level == 36:
			print "Congratulations, your Wartortle has evolved into Blastoise!"
			set_pokemon("Blastoise", "Water", "Hydro Pump")
	elif my_p_name == "Charizard" or my_p_name == "Venusaur" or my_p_name == "Blastoise":
		pass
	else:
		print "Error: my_p_name is wrong somewhere"
def fainted(area):
	global my_revives, my_p_name 
	
	print "Oh no, your %s has fainted!" % my_p_name
	stop = raw_input("... ")
	print "You and your Pokémon rush down to a Pokécenter!"
	stop = raw_input("... ")
	if my_revives == 0:
		print "Oh no, you don't have any more revives left!"
		print "Unfortunately, your Pokémon cannot be returned to you, since you we unable to take care of it."
		stop = raw_input("... ")
		print "---------- GAME OVER ----------"
		exit()
	else:
		print "You made it just in time, but unfortunately, you had to use one of your precious revives."
	stop = raw_input("... ")
	my_revives -= 1
	if my_revives > 1:
		print "You have %d more revives left. Be careful next time!" % my_revives
	elif my_revives == 1:
		print "You only have 1 revive left! You need to be especially careful!"
	else:
		print "Error: Unexpected number of revives."
		exit()
	
	stop = raw_input("... ")
	
	pokecenter()
	
	#add the Pokemon gyms once that code has been written
	if area == "route 1":
		return_loc = "palet town home"
	elif area == "veridian forest" or area == "route 2":
		return_loc = "veridian city"
	elif area == "route 3" or area == "mt moon" or area == "route 4" or area == "brock":
		return_loc = "pewter city"
	elif area == "Misty":
		return_loc = "cerulean city"
	elif area == "Brock":
		return_loc = "pewter city"
	else:
		print "Error: Invalid area argument in fainted()."
		exit()
		
	play(return_loc, "up")	
def battle(area):
	global my_p_hp, my_p_max_hp, my_p_name, this_name, this_level, this_max_attack_damage, this_hp, this_exp_value, this_attack, battle_completed
	
	battle_completed = False
	
	# different wilds in different areas
	if area == "route 1":
		wilds = ["Pidgey", "Pidgey", "Ratatta", "Ratatta", "Pikachu"]
		levels = [2, 2, 2, 3, 3, 3, 4,]
	elif area == "veridian forest":
		wilds = ["Caterpie", "Caterpie", "Metapod", "Metapod", "Pikachu"]
		levels = [2, 2, 3, 3, 3, 4, 4, 4, 5]
	elif area == "route 2":
		wilds = ["Caterpie", "Hoothoot", "Spinarak", "Nidoran", "Mr. Mime"]
		levels = [4, 4, 4, 5, 5, 6]
	elif area == "route 3":
		wilds = ["Sandshrew", "Jigglypuff", "Mankey", "Ekans", "Raticate"]
		levels = [5, 6, 6, 7, 7, 7, 8, 9]
	elif area == "mt moon":
		wilds = ["Sandshrew", "Clefairy", "Zubat", "Zubat", "Geodude"]
		levels = [7, 7, 8, 8, 8, 9, 9, 10, 11]
	elif area == "route 4":
		wilds = ["Sandshrew", "Arbok", "Spearow", "Jigglypuff", "Geodude"]
		levels = [8, 8, 9, 9, 10, 10, 11, 11, 12]
	else:
		print "Error: Improper area argument given."
			
	this_name = random.choice(wilds)
	this_level = random.choice(levels)
	# SECOND ATTACK DAMAGE/HP FORMULA
	this_max_attack_damage = this_level * 2 
	this_hp = (this_level * 5) + 20
	# WILD EXP VALUE FORUMLA
	this_exp_value = this_level * 19
	
	# list of all wilds and their attack names
	if this_name == "Pidgey" or this_name == "Hoothoot":
		this_attack = "Gust"
	elif this_name == "Ratatta" or this_name == "Caterpie" or this_name == "Metapod":
		this_attack = "Tackle"
	elif this_name == "Pikachu":
		this_attack = "Thundershock"
	elif this_name == "Spinarak":
		this_attack = "Poison Sting"
	elif this_name == "Nidoran":
		this_attack = "Double Kick"
	elif this_name == "Mr. Mime":
		this_attack = "Confusion"
	elif this_name == "Sandshrew":
		this_attack = "Scratch"
	elif this_name == "Jigglypuff" or this_name == "Clefairy":
		this_attack = "Double Slap"
	elif this_name == "Zubat":
		this_attack = "Leech Life"
	elif this_name == "Mankey":
		this_attack = "Low Kick"
	elif this_name == "Ekans":
		this_attack = "Wrap"
	elif this_name == "Raticate":
		this_attack = "Bite"
	elif this_name == "Geodude":
		this_attack = "Rock Throw"
	elif this_name == "Arbok":
		this_attack = "Acid"
	elif this_name == "Spearow":
		this_attack = "Peck"
	else:
		this_attack = "Unkown Attack!"
		
	
	def battle_choice():
		global this_level, my_p_level, battle_completed

		if not battle_completed:	
			decision = raw_input("Your move: ")
			print "..."
			if decision == "run":
				if this_level >= my_p_level:
					# chances of being able to run away safely, (only matters if wild level is the same or higher)
					can_run_options = ["safe", "safe", "safe", "safe", "safe", "safe", "can't"]
					can_run = random.choice(can_run_options)
					if can_run == "safe":
						print "You got away safely."
					else:
						print "Oh no, you couldn't get away!"
						wild_attack()
						battle_choice()
				else:
					print "You got away safely."
			elif decision == "attack":
				if this_level > my_p_level:
					wild_attack()
					stop = raw_input("... ")
					user_attack()
				else:
					user_attack()
					stop = raw_input("... ")
					wild_attack()
				
				if not battle_completed:
					print "..."
					battle_choice()
			elif decision == "potion" or decision == "heal":
				potion()
				stop = raw_input("... ")
				if potion_used:
					wild_attack()
				battle_choice()
			else:
				print "That is not currently an option."
				battle_choice()
		
		
	def wild_attack():
		global this_name, this_attack, this_max_attack_damage, my_p_name, my_p_hp, this_hp, battle_completed
	
		damage = int(math.ceil(this_max_attack_damage * random.uniform(0.5, 1.0)))
	
		if not battle_completed:
			print "The wild %s used %s, which caused %d damage to %s!" % (this_name, this_attack, damage, my_p_name)
			my_p_hp -= damage
			stop = raw_input("... ")
			if my_p_hp <= 0:
				fainted(area)
			else:	
				print "The wild %s's HP: %d" % (this_name, this_hp)
				print "%s's HP: %d" % (my_p_name, my_p_hp)
	
	def user_attack():
		global this_hp, this_name, my_p_name, my_p_hp, battle_completed, my_p_max_attack_damage
		
		damage = int(math.ceil(my_p_max_attack_damage * random.uniform(0.5, 1.0)))
		
		print "Your %s used %s, which caused %d damage to the wild %s!" % (my_p_name, my_p_attack, damage, this_name)
		this_hp -= damage
		stop = raw_input("... ")
		if this_hp <= 0: #you defeated the wild
			print "You defeated the wild %s!" % this_name
			stop = raw_input("... ")
			level_up()
			battle_completed = True
			battle_choice()
		else:	
			print "The wild %s's HP: %d" % (this_name, this_hp)
			print "%s's HP: %d" % (my_p_name, my_p_hp)

		

	#The battle taking place!
	print "A wild Level %d %s just appeared!" % (this_level, this_name)
	battle_choice()
def pokecenter():
	global my_p_hp, my_p_max_hp, my_p_name
	
	my_p_hp = my_p_max_hp
	print "Pokécenter Nurse:"
	print "Your %s is now fully healed!" % my_p_name
	stop = raw_input("... ")
	print "%s's HP is now %d." % (my_p_name, my_p_hp)
	stop = raw_input("... ")
def grass(area):
	grass_options = ["yes", "no"]
	grass_choice = random.choice(grass_options)
	if grass_choice == "yes":
		battle(area)
def potion():
	global my_potions, my_p_hp, my_p_max_hp, potion_value, my_p_name, name, potion_used
	
	potion_used = False
	
	if my_potions == 0:
		print "You don't have any potions left to use!"
	elif my_potions >= 1:
		potion_used = True
		my_potions -= 1
		my_p_hp += potion_value
		if my_p_hp > my_p_max_hp:
			difference = my_p_hp - my_p_max_hp
			my_p_hp = my_p_max_hp
		else:
			difference = 0
		print "%s's HP has increase by %d." % (my_p_name, potion_value - difference)
		print "%s's HP: %d/%d" % (my_p_name, my_p_hp, my_p_max_hp)
		print "%s's remaining potions: %d" % (name, my_potions)
def gym(leader, pokemon):
	global this_name, this_level, this_max_attack_damage, this_hp, this_exp_value, this_attack
	global my_p_name, badges, name, battle_completed
	
	battle_completed = False
	
	def gym_battle_choice():
		global this_level, my_p_level, battle_completed

		if not battle_completed:	
			decision = raw_input("Your move: ")
			print "..."
			if decision == "attack":
				if this_level > my_p_level:
					opp_attack()
					stop = raw_input("... ")
					gym_user_attack()
				else:
					gym_user_attack()
					stop = raw_input("... ")
					opp_attack()
				
				print "..."
				gym_battle_choice()
			elif decision == "potion" or decision == "heal":
				potion()
				stop = raw_input("... ")
				if potion_used:
					opp_attack()
				gym_battle_choice()
			else:
				print "That is not currently an option."
				gym_battle_choice()
		else:
			pass	
	def opp_attack():
		global this_name, this_attack, this_max_attack_damage, my_p_name, my_p_hp, this_hp, battle_completed
	
		damage = int(math.ceil(this_max_attack_damage * random.uniform(0.5, 1.0)))
	
		if not battle_completed:
			print "%s used %s, which caused %d damage to %s!" % (this_name, this_attack, damage, my_p_name)
			my_p_hp -= damage
			stop = raw_input("... ")
			if my_p_hp <= 0:
				fainted(leader)
			else:	
				print "%s's HP: %d" % (this_name, this_hp)
				print "%s's HP: %d" % (my_p_name, my_p_hp)
	def gym_user_attack():
		global this_hp, this_name, my_p_name, my_p_hp, battle_completed, my_p_max_attack_damage
		
		damage = int(math.ceil(my_p_max_attack_damage * random.uniform(0.5, 1.0)))
		
		print "Your %s used %s, which caused %d damage to %s!" % (my_p_name, my_p_attack, damage, this_name)
		this_hp -= damage
		stop = raw_input("... ")
		if this_hp <= 0: 
			print "You defeated %s's %s!" % (leader, this_name)
			stop = raw_input("... ")
			level_up()
			battle_completed = True
			gym_battle_choice()
		else:	
			print "%s's HP: %d" % (this_name, this_hp)
			print "%s's HP: %d" % (my_p_name, my_p_hp)
	def fight():
		print "%s sent out a Level %d %s!" % (leader, this_level, this_name)
		stop = raw_input("... ")
		print "Go %s!" % my_p_name
		gym_battle_choice()	

	if leader == "Misty" and pokemon == "Staryu" and badges == 1:
		this_name = pokemon
		this_level = 18
		this_attack = "Water Gun"
		this_max_attack_damage = this_level * 2
		this_hp = (this_level * 5) + 20
		this_exp_value = this_level * 19
		fight()
		gym("Misty", "Starmie")
	elif leader == "Misty" and pokemon == "Starmie" and badges == 1:
		this_name = pokemon
		this_level = 20
		this_attack = "Psychic"
		this_max_attack_damage = this_level * 2
		this_hp = (this_level * 5) + 20
		this_exp_value = this_level * 19
		fight()
		
		badges += 1
		
		print "Misty: Wow, you are cute AND strong!"
		stop = raw_input("... ")
		print "You have now earned the Cascade Badge. Congratulations!"
		stop = raw_input("... ")
		print "Anyone who beats me should report directly to Professor Oak!"
		stop = raw_input("... ")
	
	elif leader == "Brock" and pokemon == "Geodude" and badges == 0:
		this_name = pokemon
		this_level = 11
		this_attack = "Rock Throw"
		this_max_attack_damage = this_level * 2
		this_hp = (this_level * 5) + 20
		this_exp_value = this_level * 19
		fight()
		gym("Brock", "Onix")
	elif leader == "Brock" and pokemon == "Onix" and badges == 0:
		this_name = pokemon
		this_level = 13
		this_attack = "Rock Slide"
		this_max_attack_damage = this_level * 2
		this_hp = (this_level * 5) + 20
		this_exp_value = this_level * 19
		battle_completed = False
		fight()
		
		badges += 1
		
		print "Brock: That was incredible. You have some serious talent!"
		stop = raw_input("... ")
		print "You have now earned the Boulder Badge. Congratulations!"
		stop = raw_input("... ")
		print "Good luck on the rest of your journey, %s" % name
		stop = raw_input("... ")
	else:
		print "Error: Unexpected argument in gym()"
def mart():
	global my_potions
	print "Welcome to the Pokémart!"
	print "Would you like me to refill your potions for you?"
	answer = raw_input("> ").lower()
	if answer == "yes":
		print "Great! You now have 5 full potions to use."
	else:
		print "I only understand the word yes, so I refilled them anyway!"
		print "You now have 5 full potions to use."
	my_potions = 5
	stop = raw_input("... ")
			
		
def set_pokemon(name, type, attack):
	global my_p_name, my_p_level, my_p_type, my_p_attack

	my_p_name = name
	my_p_type = type
	my_p_attack = attack
	print "You now have a Level %d %s." % (my_p_level, my_p_name)
	print "Your %s can use the attack move %s." % (my_p_name, my_p_attack)
	stop = raw_input("... ")
def choose_starter():
	global chosen, my_p_name, my_p_type

	print "Who will you choose to be your companion?"
	print "Bulbasaur, Squirtle, or Charmander?"
	
	choice = raw_input("> ").lower().capitalize()
	print "..."
	if choice == "Bulbasaur":
		type = "Grass"
		attack = "Vine Whip"
		set_pokemon(choice, type, attack)
	elif choice == "Squirtle":
		type = "Water"
		attack = "Water Gun"
		set_pokemon(choice, type, attack)
	elif choice == "Charmander":
		type = "Fire"
		attack = "Ember"
		set_pokemon(choice, type, attack)
	else:
		print "That's not a choice, you silly lad!"
		print "Try again.\n"
		choose_starter()
	print oak 
	print "You chose the %s type Pokémon, %s." % (my_p_type.lower(), my_p_name)
	print "What a marvelous choice!"
	chosen = True
	stop = raw_input("... ")
	

	
	
start()
