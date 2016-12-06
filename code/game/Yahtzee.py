from random import randint
import os
import sys

global score
score = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], ["Three of A kind", 0],
         ["Four of A Kind", 0], ["Full House", 0], ["Small Straight", 0],
         ["Large Straight", 0], ["Yahtzee", 0], ["Chance", 0], ["Total points", 0], ["Total Part 1", 0],
         ["Total Part 2", 0], ["Total", 0]]


def menu():
    clearscreen()
    correct = False
    while not correct:
        print("Welcome to Yahtzee \n- Menu Yahtzee - \nSingle player  (S)\nMulti player   (M)\nQuit          (Q)")
        try:
            choice = input("\nChoose one (S, M, of Q): ")
            if choice.upper() == "S":
                clearscreen()
                correct = True
                playyahtzee()
            elif choice.upper() == "M":
                clearscreen()
                print("Multi player is under construction")
                correct = False
            elif choice.upper() == "Q":
                sys.exit()
        except(KeyboardInterrupt, ValueError):
            clearscreen()
            print("You made a wrong decision")


def playyahtzee():
    global dices
    global stage
    stage = 13
    while stage < 14:
        clearscreen()
        turn = 1
        dices = []
        saved_dices = []
        while turn < 4:
            clearscreen()
            teller = 0
            for b in range(5 - len(dices)):
                thrown_dice = randint(1, 6)
                dices.append(thrown_dice)
            if turn < 3:
                print("Stage:", stage, "\nTurn:", turn,"\nThrown dices:")
                for c in range(len(dices)):
                    if c == (len(dices) - 1):
                        print(dices[c], end="")
                    else:
                        print(dices[c], end=", ")
                for d in range(len(dices)):
                    print("\n", "Dice with value: ", dices[d], sep="")
                    choice = False
                    while not choice:
                        try:
                            bewaren = str(input("Do you want to keep this dice? (Y/N): "))
                            if bewaren.upper() == "Y":
                                teller += 1
                                choice = True
                                print(dices[d], "is being saved")
                                saved_dices.append(dices[d])
                                if teller == 5:
                                    turn = 4
                            elif bewaren.upper() == "N":
                                print(dices[d], "is being deleted")
                                choice = True
                            else:
                                print("You made a wrong decision")
                        except(KeyboardInterrupt, ValueError):
                            print("You made a wrong decision")
                if len(saved_dices) != 5:
                    dices.clear()
                    for e in range(len(saved_dices)):
                        dices.append(saved_dices[e])
                    saved_dices.clear()
            turn += 1
        fillscore()
        stage += 1
    printscore()


def fillscore():
    clearscreen()
    dices.sort()
    correct = False
    while not correct:
        print("Your finaly thrown dices:")
        for i in range(len(dices)):
            if i == (len(dices) - 1):
                print(dices[i], end="")
            else:
                print(dices[i], end=", ")
        print("""\nChoose where you want to fill in your score \n- Menu Score -
1.  Aces\n2.  Twos\n3.  Threes\n4.  Fours\n5.  Fives\n6.  Sixes\n\n7.  Three of A Kind\n8.  Four of A Kind
9.  Full House\n10. Small Straight\n11. Large Straight\n12. Yahtzee\n13. Chance""")
        try:
            choice = int(input("\nChoose one (1 to 13 inclusive): "))
            i = choice - 1
            if choice < 7:
                if score[i][1] != 0:
                    clearscreen()
                    correct = False
                    print("You already have filled in this one, choose another one")
                elif score[i][0] not in dices:
                    clearscreen()
                    print("You didn't throw", score[i][0])
                    choice_jn = input("Do you want to leave this empty? (Y/N): ")
                    if choice_jn.upper() == "Y":
                        score[i][1] = "x"
                    elif choice_jn.upper() == "N":
                        correct = False
                else:
                    correct = True
                    amount = dices.count(choice)
                    total = amount * score[i][0]
                    score[i][1] = total
            if choice >= 7:
                if score[i][1] != 0:
                    clearscreen()
                    correct = False
                    print("You already have filled in this one, choose another one")
                else:
                    correct = True
                    if choice == 7:
                        a = 1
                        while a < 7:
                            amount_a = dices.count(a)
                            if amount_a == 3:
                                som = 0
                                for b in range(len(dices)):
                                    som += dices[b]
                                score[i][1] = som
                            a += 1
                        if score[i][1] == 0:
                            clearscreen()
                            choice_jn = input(
                                "You don't have Three of A Kind, do you want to leave this empty? (Y/N): ")
                            if choice_jn.upper() == "Y":
                                score[i][1] = "x"
                            elif choice_jn.upper() == "N":
                                correct = False
                    elif choice == 8:
                        a = 1
                        while a < 7:
                            amount_a = dices.count(a)
                            if amount_a == 4:
                                som = 0
                                for b in range(len(dices)):
                                    som += dices[b]
                                score[i][1] = som
                            a += 1
                        if score[i][1] == 0:
                            clearscreen()
                            choice_jn = input("You don't have Four of A Kind, do you want to leave this empty? (Y/N): ")
                            if choice_jn.upper() == "Y":
                                score[i][1] = "x"
                            elif choice_jn.upper() == "N":
                                correct = False
                    elif choice == 9:
                        a = 1
                        while a < 7:
                            amount_a = dices.count(a)
                            if amount_a == 3:
                                b = 1
                                while b < 7:
                                    if b == a:
                                        b += 1
                                    amount_b = dices.count(b)
                                    if amount_b == 2:
                                        score[i][1] = 25
                                        b = 7
                                    else:
                                        b += 1
                            a += 1
                        if score[i][1] == 0:
                            clearscreen()
                            choice_jn = input("You don't have Full House, do you want to leave this empty? (Y/N): ")
                            if choice_jn.upper() == "Y":
                                score[i][1] = "x"
                            elif choice_jn.upper() == "N":
                                correct = False
                    elif choice == 10:
                        for b in range(3):
                            for c in range(6):
                                kleine_straat = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]
                                kleine_straat[b].append(c + 1)
                                kleine_straat[b].sort()
                                if kleine_straat[b] == dices:
                                    score[i][1] = 30
                        if score[i][1] == 0:
                            clearscreen()
                            choice_jn = input("You don't have small straight, do you want to leave this empty? (Y/N): ")
                            if choice_jn.upper() == "Y":
                                score[i][1] = "x"
                            elif choice_jn.upper() == "N":
                                correct = False
                    elif choice == 11:
                        if dices == [1, 2, 3, 4, 5] or dices == [2, 3, 4, 5, 6]:
                            score[i][1] = 40
                        if score[i][1] == 0:
                            clearscreen()
                            choice_jn = input("You don't have large straight, do you want to leave this empty? (Y/N): ")
                            if choice_jn.upper() == "Y":
                                score[i][1] = "x"
                            elif choice_jn.upper() == "N":
                                correct = False
                    elif choice == 12:
                        a = 1
                        while a < 7:
                            amount_a = dices.count(a)
                            if amount_a == 5:
                                score[i][1] = 50
                            a += 1
                        if score[i][1] == 0:
                            clearscreen()
                            choice_jn = input("You don't have Yathzee, do you want to leave this empty? (Y/N): ")
                            if choice_jn.upper() == "Y":
                                score[i][1] = "x"
                            elif choice_jn.upper() == "N":
                                correct = False
                    elif choice == 13:
                        som = 0
                        for a in range(len(dices)):
                            som += dices[a]
                        score[i][1] = som
        except(KeyboardInterrupt, ValueError):
            clearscreen()
            print("You made a wrong decision")
    printscore()


def printscore():
    clearscreen()
    if stage == 14:
        som = 0
        for b in range(6):
            som += score[b][1]
        score[13][1] = som
        if som >= 63:
            score[14][1] = som + 35
        else:
            score[14][1] = score[13][1]
        som = 0
        for c in range(6):
            if score[c + 6][1] == "x":
                c += 1
            som += score[c + 6][1]
        score[15][1] = som
        score[16][1] = score[14][1] + score[15][1]
    print("\nYour score:\nPart 1")
    for a in range(len(score)):
        if a < 6:
            print("All", score[a][0], "           |", score[a][1])
        elif a == 6:
            if stage == 14:
                print(score[13][0], "    |", score[13][1])
            print("\nPart 2")
            print(score[a][0], " |", score[a][1])
        elif a == 7:
            print(score[a][0], "  |", score[a][1])
        elif a == 8:
            print(score[a][0], "      |", score[a][1])
        elif a == 9:
            print(score[a][0], "  |", score[a][1])
        elif a == 10:
            print(score[a][0], "  |", score[a][1])
        elif a == 11:
            print(score[a][0], "         |", score[a][1])
        elif a == 12:
            print(score[a][0], "          |", score[a][1])
    if stage == 14:
        print("\n", score[14][0], "     | ", score[14][1], "\n", score[15][0], "     | ", score[15][1], "\n", score[16][0],
              "            | ", score[16][1], sep="")
        input("Press enter to return to the menu")
    if stage != 14:
        input("Press enter to continue")


def clearscreen():
    os.system("cls")


play = True
while play:
    menu()
