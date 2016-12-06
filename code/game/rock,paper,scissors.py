#Python 2 

import time
import random
import os



player_score = 0
comp_score = 0
    

while True:
    choicescomp = ["rock","paper","scissors"]
    cfc = random.choice(choicescomp)
    ufc = raw_input("rock,paper,or scissors?")
    wait = time.sleep
    if ufc == "rock" and cfc == "scissors":
        wait(.5)
        print("The computer chose " + cfc)
        wait(1)
        print("You win!")
        player_score += 1
        wait(1)
        print("Your score:" + str(player_score))
        print("Computer score:" + str(comp_score))
        wait(.5)
    elif ufc == "scissors" and cfc == "rock":
        wait(.5) 
        print("The computer chose rock!")
        wait(1)
        print("You lose!")
        comp_score += 1
        wait(1)
        print("Your score:" + str(player_score))
        print("Computer score:" + str(comp_score))
        wait(.5)
    
    elif ufc == "paper" and cfc == "rock":
        wait(.5)
        print("The computer chose rock!")
        wait(1)
        print("You win!")
        player_score += 1
        wait(1)
        print("Your score:" + str(player_score))
        print("Computer score:" + str(comp_score))
        wait(.5)
    elif ufc == "rock" and cfc == "paper":
        wait(.5)
        print("The computer chose paper!")
        wait(1)
        print("You lose!")
        comp_score += 1
        wait(1)
        print("Your score:" + str(player_score))
        print("Computer score:" + str(comp_score))
        wait(.5)
    elif ufc == "rock" and cfc == "rock":
        wait(.5)
        print("The computer chose rock!")
        wait(1)
        print("Tie!")
        wait(1)
        print("Your score:" + str(player_score))
        print("Computer score:" + str(comp_score))
        wait(.5)
    elif ufc == "paper" and cfc == "scissors":
        wait(.5)
        print("The computer chose scissors!")
        wait(1)
        print("You win!")
        player_score += 1
        wait(1)
        print("Your score:" + str(player_score))
        print("Computer score:" + str(comp_score))
        wait(.5)
    elif ufc == "paper" and cfc == "paper":
        wait(.5)
        print("The computer chose paper")
        wait(1)
        print("Tie!")
        wait(1)
        print("Your score:" + str(player_score))
        print("Computer score:" + str(comp_score))
        wait(.5)
        
    elif ufc == "scissors" and cfc == "paper":
        
        wait(.5)
        print("The computer chose paper!")
        wait(1)
        print("You win!")
        
        player_score += 1
        wait(1)
        print("Your score:" + str(player_score))
        print("Computer score:" + str(comp_score))
        wait(.5)
    elif ufc == "scissors" and cfc == "scissors":
        wait(.5)
        print("The computer chose scissors")
        wait(1)
        print("It's a tie!")
        wait(1)
        
        
        print("Your score:" + str(player_score))
        print("Computer score:" + str(comp_score))
        wait(.5)
        
    else:
        wait(.5)
        print("Not a valid choice!")
        wait(.5)
