scenes = [
    
  ["""Welcome to trailz, an interactive text game. The rules are simple, you will be given a scenario, and can type whatever is in the parentheses.  Good luck!
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  Help: to pick up and item, type "take" and that particular items name. To check your inventory, type "list items".
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  You are walking on a wooden trail and notice you are lost, and soon arrive at a crossroads right before huge trees fall across the path you have been walking on, so you may not turn back.  Do you want to: (1) Go along the east path, (2) Go along the west path, or (3) Go along the north path.""", 5, 6, 7], 
  #This is the crossroads from the east: 1
  ["You again arrive at the crossroads.  Do you want to: (1) Go along the north path, or (2) Go along the west path.", 7, 6],
  #this is from the west: 2
  ["You again arrive at the crossroads.  Do you want to: (1) Go along the east path, or (2) Go along the north path.", 5, 7],
  #this is from the north: 3
  ["You again arrive at the crossroads.  Do you want to: (1) Go along the east path, or (2) Go along the west path.", 5, 6],
  #4
  ["You died!"],
  #5
  ["You begin to walk along the east path, and soon arrive at a small log cabin.  Do you want to: (1) Enter the small cabin, or (2) Walk back towards the crossroads.", 8, 1],
  #6
  ["You begin to walk along the west path, and soon arrive at a raging water fall, and notice a piece of the bridge is missing.  Do you want to: (1) Place the plank, (2) Walk back towards the crossroads, or (3) try and swim across.", 0, 2, 4],
  #7
  ["You begin to walk along the north path, and soon arrive at a large brick and mortar building.  Do you want to: (1) Enter the large building, or (2) Walk back towards the crossroads.", 13, 3],
  #8 east
  ["You enter the small cabin and see two doors.  Do you want to: (1) Go into the right door, (2) Walk into the left door, or (3) Walk back outside.", 10, 9, 11],
  #9
  ["You enter the left door.  Do you want to: (1) Walk back out into the main room.", 12],
  #10
  ["You enter the right door.  Do you want to: (1) Walk back out into the main room.", 12],
  #11
  ["You walk outside the cabin.  Would you like to: (1) Enter the small cabin, or (2) Walk back towards the crossroads.", 8, 1],
  #12
  ["You walk back into the main room.  Do you want to: (1) Go into to the right door, (2) Go into the left door, or (3) Walk back outside.", 10, 9, 11],
  #13 north
  ["You enter the large building and see a white, bloody double door in front of you, and a staircase to your left.  Do you want to: (1) Go into the white double doors, or (2) walk upstairs.", 14, 15],
  #14
  ["You enter the doors and walk into what appears to be an old surgical center.  Do you want to: (1) Go back into the main room", 16],
  #15 needs candle
  ["You walk up the stairs, and it is pitch black Do you want to: (1) walk back downstairs.", 16],
  #16
  ["You walk back into the main room. Do you want to: (1) Walk into the double doors, or (2) walk upstairs.", 14, 15]
]
 
 
 
 
 
 
####################
items = []
room_contents = ["","","","","","","","","","plank","candle","","","","knife","",""]
####################
 
scene_num = 0
 
while scene_num != 4:
	print scenes[scene_num][0]
	if room_contents[scene_num] != "":
		print "There is a %s in this room" %room_contents[scene_num]
	choice = raw_input("> ")
	if len(choice.split()) > 1:
		if choice.split()[0] == "take":
			if choice.split()[1]==room_contents[scene_num]:
				items.append(room_contents[scene_num])
				room_contents[scene_num] = ""
			else:
				print "I don't see that item in this room."
		elif choice.split()[0] == "list":
			if choice.split()[1] == "items":
				print "Your items are: %s" %", ".join(items)
	else:
		choice = int(choice)
		scene_num = scenes[scene_num][choice]
else:
	print "You died!"
