from sys import exit

def basement():
    print "You are in a dank and dirty basement."
    print "Your goal is to escape the house alive.  Good luck."
    print "You see a set of stairs."
    print "Go up the stairs or do nothing?"
    
    next = raw_input("Stairs or do nothing?  ")
    
    if "stair" in next:
        first_floor()
    elif "nothing" in next:
        end("You die from starvation.") 
    else:
        print "That's not an option."
        
        
def first_floor():
    print "There are 3 doors here."
    print "One is straight ahead, one is on your right, and one on your left."
    
    next = raw_input("straight, right, or left?  ")
    
    if "straight" in next:
        alligator_room()
    elif "right" in next:
        plant_room()
    elif "left" in next:
        dark_room()
    elif "stair" in next:
        basement()
    else:
        end("You die from indecisiveness")
       
def alligator_room():
    end("You fall into a pool of water 15 feet below the door where countless alligators eat your body")
    
def plant_room():
    print "THERE'S A GIANT GENETICALLY MONSTROUSLY MODIFIED PLANT READY TO EAT YOU!!!"
    zombie = False 
    
    while True:
        next = raw_input("FLEE OR FIGHT?!  ")
    
        if next == "flee":
            print "Good idea!"
            first_floor()
        elif next == "fight" and not zombie:
            print "The plant bites you and you turn into a zombie!"
            print "You can still flee before it finishes you off!"
            zombie = True 
        
            next2 = raw_input("Flee or fight?!  ")
        
            if "flee" in next2:
                print "Good idea!"
                first_floor()
            if "fight" in next2:
                end("Why?!")
                
def dark_room():
    print "You can't see anything!  It's too dark!"
    
    next = raw_input("Straight, left, or right?  ")
    
    if "straight" in next:
        end("You fall into an abyss.")
    elif "right" in next:
        end("A nest of vipers greet you warmly with THEIR FANGS AND BITE YOU TO DEATH.")
    elif "back" in next:
        first_floor()
    elif "left" in next:
        freedom()
    else:
        print "You wander into the endless depths of the room, never to be heard from again."
        end("I assume you died.")
        
def freedom():
    print "You're free! FREE!"
    print "But wait... did you turn into a zombie???"
    
    next = raw_input("Yes or no?  ")
    
    if "yes" in next:
        end("You started a zombie apocalypse!!!")
    elif "no" in next:
        print "You win!"
        print "You get to live the rest of your life forgetting the horrors you have seen."
        exit(0)

        
def end(lose):
    print lose, "You lose :("
    print "Start again or exit?"
    
    next = raw_input("> ")
    
    if "start" in next or "again" in next:
        basement()
    else:
        exit(0)
    
basement()
