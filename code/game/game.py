import random
if __name__ == "__main__":
    # this decides whether the user wants to continue
    choice = True

    # the main game loop
    while choice:
        print "Random number: " + str(random.random() * 100)
        print "Do you want to continue? Y/N?: ", 
        user_choice = raw_input()
        if user_choice == 'n' or user_choice == "N":
            print "Thanks for playing!!!"
            choice = False
