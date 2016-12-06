import os
def clear():
    os.system('cls')
def draw_table(a):
    for i in range(3):
        print("-------")
        for j in range(1,4):
            print("|", end="")
            print(a[i*3+j-1], end="")
            if j == 3:
                print("|", end="")
                print()
def move(name):
    onemove = int(input("Your move "+name+":"))
    return onemove
def checkwin(table):
    x = 0
    if ((table[0] == table[3] == table[6]) or (table[1] == table[4] == table[7]) or (table[2] == table[5] == table[8]) or(table[0] == table[4] == table[8]) or (table[2] == table[4] == table[6]) or (table[0]==table[1] == table[2]) or (table[6]==table[7] == table[8]) or (table[3]==table[4] == table[5])):
        print("we have a winner")
        x = 1
    return x
def game():
    table = []
    win = 0
    for i in range(1,10):
        table.append(i)
    draw_table(table)
    while win == 0:
        moveX = move("X")
        if str(table[moveX - 1]) not in "XO":
            table[moveX - 1 ] = "X"
        clear()
        draw_table(table)
        win = checkwin(table)
        if win == 1:
            break
        moveY = move("0")
        if str(table[moveY - 1]) not in "XO":
            table[moveY - 1] = "O"
        clear()
        draw_table(table)
        win = checkwin(table)
play = 1
while play == 1:
    play = 0
    game()
    play = int(input("If you wanna stop playing write 1:"))
