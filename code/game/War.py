import random
from tkinter import *
import tkinter
import time
import gc

gc.disable()
tk = Tk()
tk.geometry('300x100')
canvas = Canvas(tk, width=1100, height=400, bg = 'dark green')
canvas.pack()
canvas.pack(expand = YES, fill = BOTH)

message = '''Card Game: War.
             Both players play a card at random, higher card wins.
             If there is a tie, no points are awarded.'''


#Your Score
canvas.create_text(100,300, text='Your Points:')
canvas.create_text(1070,300, text="Computer Points:")


#Card in the top left
gif1 = PhotoImage(file = 'card_top_left.gif')
canvas.create_image(50, 10, image = gif1, anchor = NW)
canvas.create_text(110, 220, text='Your deck of cards')
        
#Card in top right
gif2 = PhotoImage(file = 'card_top_right.gif')
canvas.create_image(1000, 10, image = gif2, anchor = NW)
canvas.create_text(1070, 220, text='Computer\'s deck of cards')

#text for drawn card
canvas.create_text(850,220, text='Computer\'s card')
canvas.create_text(270, 220, text='Your card')



def main():
    num=computer_guess()
    number=user_guess()
    
def computer_guess():
    num=random.randrange(2,14)
    
    if num==2:
       gif3 = PhotoImage(file = 'two_of_hearts.gif')
       canvas.create_image(800, 10, image = gif3, anchor = NW)
       label = Label(image=gif3)
       label.image = gif3 
       label.pack()
    if num==3:
       gif4 = PhotoImage(file = 'three_of_hearts.gif')
       canvas.create_image(800, 10, image = gif4, anchor = NW)
       label = Label(image=gif4)
       label.image = gif4 
       label.pack()
    if num==4:
       gif5 = PhotoImage(file = 'four_of_hearts.gif')
       canvas.create_image(800, 10, image = gif5, anchor = NW)
       label = Label(image=gif5)
       label.image = gif5 
       label.pack()
    if num==5:
       gif6 = PhotoImage(file = 'five_of_diamonds.gif')
       canvas.create_image(800, 10, image = gif6, anchor = NW)
       label = Label(image=gif6)
       label.image = gif6 
       label.pack()
    if num==6:
       gif7 = PhotoImage(file = 'six_of_spades.gif')
       canvas.create_image(800, 10, image = gif7, anchor = NW)
       label = Label(image=gif7)
       label.image = gif7 
       label.pack()
    if num==7:
       gif8 = PhotoImage(file = 'seven_of_spades.gif')
       canvas.create_image(800, 10, image = gif8, anchor = NW)
       label = Label(image=gif8)
       label.image = gif8 
       label.pack()
    if num==8:
       gif9 = PhotoImage(file = 'eight_of_clubs.gif')
       canvas.create_image(800, 10, image = gif9, anchor = NW)
       label = Label(image=gif9)
       label.image = gif9 
       label.pack()
    if num==9:
       gif10 = PhotoImage(file = 'nine_of_hearts.gif')
       canvas.create_image(800, 10, image = gif10, anchor = NW)
       label = Label(image=gif10)
       label.image = gif10 
       label.pack()
    if num==10:
       gif11 = PhotoImage(file = 'ten_of_clubs.gif')
       canvas.create_image(800, 10, image = gif11, anchor = NW)
       label = Label(image=gif11)
       label.image = gif11 
       label.pack()
    if num==11:
       gif12 = PhotoImage(file = 'jack_of_diamonds.gif')
       canvas.create_image(800, 10, image = gif12, anchor = NW)
       label = Label(image=gif12)
       label.image = gif12 
       label.pack()
    if num==12:
       gif13 = PhotoImage(file = 'queen_of_hearts.gif')
       canvas.create_image(800, 10, image = gif13, anchor = NW)
       label = Label(image=gif13)
       label.image = gif13 
       label.pack() 
    if num==13:
       gif14 = PhotoImage(file = 'king_of_spades.gif')
       canvas.create_image(800, 10, image = gif14, anchor = NW)
       label = Label(image=gif14)
       label.image = gif14 
       label.pack()
    if num==14:
       gif15 = PhotoImage(file = 'ace_of_diamonds.gif')
       canvas.create_image(800, 10, image = gif15, anchor = NW)
       label = Label(image=gif15)
       label.image = gif15 
       label.pack()

    return num

def user_guess():
    number=random.randrange(2,14)
    num=computer_guess()
    
    if number==2:
       gif3 = PhotoImage(file = 'two_of_hearts.gif')
       canvas.create_image(230, 10, image = gif3, anchor = NW)
       label = Label(image=gif3)
       label.image = gif3 
       label.pack()
       if num > 2:
           canvas.create_text(1125, 300, text='1')
       elif num == 2:
           qw=canvas.create_text(600, 200, text="Draw: No Points Awarded")
           tk.update()
           canvas.after(400)
           canvas.delete(qw)
    if number==3:
       gif4 = PhotoImage(file = 'three_of_hearts.gif')
       canvas.create_image(230, 10, image = gif4, anchor = NW)
       label = Label(image=gif4)
       label.image = gif4 
       label.pack()
       if num > 3:
           canvas.create_text(1132, 300, text='1')
       elif num == 3:
           qe=canvas.create_text(600, 200, text="Draw: No Points Awarded")
           tk.update()
           canvas.after(1000)
           canvas.delete(qe)
           
       else:
           canvas.create_text(140, 300, text="1")

    if number==4:
       gif5 = PhotoImage(file = 'four_of_hearts.gif')
       canvas.create_image(230, 10, image = gif5, anchor = NW)
       label = Label(image=gif5)
       label.image = gif5 
       label.pack()
       if num > 4:
           canvas.create_text(1139, 300, text='1')
       elif num == 4:
           qr=canvas.create_text(600, 200, text="Draw: No Points Awarded")
           tk.update()
           canvas.after(1000)
           canvas.delete(qr)
       else:
           canvas.create_text(147, 300, text="1")

    if number==5:
       gif6 = PhotoImage(file = 'five_of_diamonds.gif')
       canvas.create_image(230, 10, image  = gif6, anchor = NW)
       label = Label(image=gif6)
       label.image = gif6 
       label.pack()
       if num > 5:
           canvas.create_text(1146, 300, text='1')
       elif num == 5:
           qt=canvas.create_text(600, 200, text="Draw: No Points Awarded")
           tk.update()
           canvas.after(1000)
           canvas.delete(qt)
       else:
           canvas.create_text(154, 300, text="1")

    if number==6:
       gif7 = PhotoImage(file = 'six_of_spades.gif')
       canvas.create_image(230, 10, image = gif7, anchor = NW)
       label = Label(image=gif7)
       label.image = gif7 
       label.pack()
       if num > 6:
           canvas.create_text(1153, 300, text='1')
       elif num == 6:
           qy=canvas.create_text(600, 200, text="Draw: No Points Awarded")
           tk.update()
           canvas.after(1000)
           canvas.delete(qy)
       else:
           canvas.create_text(161, 300, text="1")
    if number==7:
       gif8 = PhotoImage(file = 'seven_of_spades.gif')
       canvas.create_image(230, 10, image = gif8, anchor = NW)
       label = Label(image=gif8)
       label.image = gif8 
       label.pack()
       if num > 7:
           canvas.create_text(1160, 300, text='1')
       elif num == 7:
           qu=canvas.create_text(600, 200, text="Draw: No Points Awarded")
           tk.update()
           canvas.after(1000)
           canvas.delete(qu)
       else:
           canvas.create_text(168, 300, text="1")       
    if number==8:
       gif9 = PhotoImage(file = 'eight_of_clubs.gif')
       canvas.create_image(230, 10, image = gif9, anchor = NW)
       label = Label(image=gif9)
       label.image = gif9 
       label.pack()
       if num > 8:
           canvas.create_text(1167, 300, text='1')
       elif num == 8:
           qicanvas.create_text(600, 200, text="Draw: No Points Awarded")
           tk.update()
           canvas.after(1000)
           canvas.delete(qi)
       else:
           canvas.create_text(175, 300, text="1") 
    if number==9:
       gif10 = PhotoImage(file = 'nine_of_hearts.gif')
       canvas.create_image(230, 10, image = gif10, anchor = NW)
       label = Label(image=gif10)
       label.image = gif10 
       label.pack()
       if num > 9:
           canvas.create_text(1174, 300, text='1')
       elif num == 9:
           qo=canvas.create_text(600, 200, text="Draw: No Points Awarded")
           tk.update()
           canvas.after(1000)
           canvas.delete(qo)
       else:
           canvas.create_text(182, 300, text="1") 
    if number==10:
       gif11 = PhotoImage(file = 'ten_of_clubs.gif')
       canvas.create_image(230, 10, image = gif11, anchor = NW)
       label = Label(image=gif11)
       label.image = gif11 
       label.pack()
       if num > 10:
           canvas.create_text(1181, 300, text='1')
       elif num == 10:
           qp=canvas.create_text(600, 200, text="Draw: No Points Awarded")
           tk.update()
           canvas.after(1000)
           canvas.delete(qp)
       else:
           canvas.create_text(189, 300, text="1") 
    if number==11:
       gif12 = PhotoImage(file = 'jack_of_diamonds.gif')
       canvas.create_image(230, 10, image = gif12, anchor = NW)
       label = Label(image=gif12)
       label.image = gif12 
       label.pack()
       if num > 11:
           canvas.create_text(1189, 300, text='1')
       elif num == 11:
           qa=canvas.create_text(600, 200, text="Draw: No Points Awarded")
           tk.update()
           tk.after(1000)
           tk.delete(qa)
       else:
           canvas.create_text(196, 300, text="1") 
    if number==12:
       gif13 = PhotoImage(file = 'queen_of_hearts.gif')
       canvas.create_image(230, 10, image = gif13, anchor = NW)
       label = Label(image=gif13)
       label.image = gif13 
       label.pack()
       if num > 12:
           canvas.create_text(1196, 300, text='1')
       elif num == 12:
           qs=canvas.create_text(600, 200, text="Draw: No Points Awarded")
           tk.update()
           canvas.after(1000)
           canvas.delete(qs)
       else:
           canvas.create_text(203, 300, text="1")
    if number==13:
       gif14 = PhotoImage(file = 'king_of_spades.gif')
       canvas.create_image(230, 10, image = gif14, anchor = NW)
       label = Label(image=gif14)
       label.image = gif14 
       label.pack()
       if num > 13:
           canvas.create_text(1203, 300, text='1')
       elif num == 13:
           qd=canvas.create_text(600, 200, text="Draw: No Points Awarded")
           tk.update()
           canvas.after(1000)
           canvas.delete(qd)
       else:
           canvas.create_text(210, 300, text="1")
    if number==14:
       gif15 = PhotoImage(file = 'ace_of_diamonds.gif')
       canvas.create_image(230, 10, image = gif15, anchor = NW)
       label = Label(image=gif15)
       label.image = gif15 
       label.pack()
       if num > 14:
           canvas.create_text(1210, 300, text='1')
       elif num == 14:
           qfcanvas.create_text(600, 200, text="Draw: No Points Awarded")
           tk.update()
           canvas.after(1000)
           canvas.delete(qf)
       else:
           canvas.create_text(217, 300, text="1")
    return number

def end():
    tk.destroy()
    
    main()

    

#Button Code
Label(tk, text=message).pack()
Button(tk, text='Play',command=main, width=10, height=10).pack(side=TOP)
Label(tk, text=message).pack()
Button(tk, text='End Game',command=end, width=10, height=10).pack(side=BOTTOM)

tk.mainloop()
