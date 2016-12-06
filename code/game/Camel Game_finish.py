print("Welcome to Camel!","\nYou have stolen a camel to make your way across the great Mobi desert.","\nThe natives want their camel back and are chasing you down! Survive your","\ndesert trek and out run the natives.")
import random
done = False
miles_traveled = 0
thirst = 0
camel_tired = 0
natives_traveled = -20
drink = 5
natives_up = random.randrange(0, 10)
full_speed = random.randrange(10, 20)
moderate_speed = random.randrange(5, 12)

while not done:
    print("A. Drink from your canteen .","\nB. Ahead moderate speed.","\nC. Ahead full speed.","\nD. Stop for the night.","\nE. Status check.","\nQ. Quit.")
    choice = input("Your choiche? ")
    if choice == "q":
        done = True
    #status_check
    elif choice == "e":
        print ("\nMiles traveled: %d\nDrinks in canteen: %d\nThe natives are %d behind you. \nCamel tiredness %d \nThirst level are %d" %(miles_traveled, drink, natives_traveled, camel_tired, thirst,))
    #stop_for_the_night
    elif choice == "d":
        camel_tired = 0
        print ("The camel is happy! and move the natives up %d miles" %(natives_up,))
    #full_speed
    elif choice == "c":
        print ("you have traveled %d miles" %(full_speed,))
        miles_traveled = miles_traveled + full_speed
        natives_traveled = natives_traveled + natives_up
        thirst = thirst + 1
        camel_tired = random.randrange(1,3)
        print ("camel tiredness %d" %(camel_tired,))
        print ("move the natives up to %d miles" %(natives_up,))
    #moderate_speed
    elif choice == "b":
        print ("you have traveled %d miles" %(moderate_speed,))
        miles_traveled += full_speed
        natives_traveled += natives_up
        thirst += 1
        camel_tired = camel_tired + random.randrange(1,3)
        print ("camel tiredness %d" %(camel_tired,))
        print ("move the natives up to %d miles" %(natives_up,))
    #drink_to_canteen
    elif choice == "a":
        print ("you drink from your canteen")
        drink = drink - 1
        thirst = 0
        

    #you are thirst
    if thirst >= 3 :
        print ("you are thirsty!!!!!")

    #you died of thirst!
    if thirst >= 5 :
        print ("you died of thirsty!!!")
        done = True

    #your camel is getting tired!
    if camel_tired >= 5:
        print ("your camel is getting tired")

    #your camel is dead
    if camel_tired >= 8:
        print ("Your camel is dead")
        done = True

    #if the natives have caught up
    if natives_traveled >= 0:
        print ("The natives caught you")
        done = True

    #the natives are walking
    elif natives_traveled >= -10:
        print ("The natives getting close")

    if miles_traveled == 300:
        print ("You won and you got the camel arround the mobi desert")
        done = True

    if drink <= 0:
        print ("The drink are out of stock!!!")
        thirst = 0
        drink = done
        
    elif thirst >= 1:
        miles_traveled -= 1
