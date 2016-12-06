# Created by: Victoria Le
# Created on: Nov,2016
# Created for: ICS3U
# This program is a game of 21 program

import ui
from numpy import random

cA = ui.Image.named('card:ClubsA')
c2= ui.Image.named('card:Clubs2')
c3 = ui.Image.named('card:Clubs3')
c4 = ui.Image.named('card:Clubs4')
c5 = ui.Image.named('card:Clubs5')
c6 = ui.Image.named('card:Clubs6')
c7 = ui.Image.named('card:Clubs7')
c8 = ui.Image.named('card:Clubs8')
c9 = ui.Image.named('card:Clubs9')
c10 = ui.Image.named('card:Clubs10')
cK = ui.Image.named('card:ClubsK')
cQ = ui.Image.named('card:ClubsQ')
cJ = ui.Image.named('card:ClubsJ')
sA = ui.Image.named('card:SpadesA')
s2 = ui.Image.named('card:Spades2')
s3 = ui.Image.named('card:Spades3')
s4 = ui.Image.named('card:Spades4')
s5 = ui.Image.named('card:Spades5')
s6 = ui.Image.named('card:Spades6')
s7 = ui.Image.named('card:Spades7')
s8 = ui.Image.named('card:Spades8')
s9 = ui.Image.named('card:Spades9')
s10 = ui.Image.named('card:Spades10')
sK = ui.Image.named('card:SpadesK')
sQ = ui.Image.named('card:SpadesQ')
sJ = ui.Image.named('card:SpadesJ')
hA = ui.Image.named('card:HeartsA')
h2 = ui.Image.named('card:Hearts2')
h3 = ui.Image.named('card:Hearts3')
h4 = ui.Image.named('card:Hearts4')
h5 = ui.Image.named('card:Hearts5')
h6 = ui.Image.named('card:Hearts6')
h7 = ui.Image.named('card:Hearts7')
h8 = ui.Image.named('card:Hearts8')
h9 = ui.Image.named('card:Hearts9')
h10 = ui.Image.named('card:Hearts10')
hK = ui.Image.named('card:HeartsK')
hQ = ui.Image.named('card:HeartsQ')
hJ = ui.Image.named('card:HeartsJ')
dA = ui.Image.named('card:DiamondsA')
d2 = ui.Image.named('card:Diamonds2')
d3 = ui.Image.named('card:Diamonds3')
d4 = ui.Image.named('card:Diamonds4')
d5 = ui.Image.named('card:Diamonds5')
d6 = ui.Image.named('card:Diamonds6')
d7 = ui.Image.named('card:Diamonds7')
d8 = ui.Image.named('card:Diamonds8')
d9 = ui.Image.named('card:Diamonds9')
d10 = ui.Image.named('card:Diamonds10')
dK = ui.Image.named('card:DiamondsK')
dQ = ui.Image.named('card:DiamondsQ')
dJ = ui.Image.named('card:DiamondsJ')

deck = [cA,c10,c9,c8,c7,c6,c5,c4,c3,c2,cK,cQ,cJ,sA,s10,s9,s8,s7,s6,s5,s4,s3,s2,sK,sQ,sJ,hA,h10,h9,h8,h7,h6,h5,h4,h3,h2,hK,hQ,dJ,dA,d10,d9,d8,d7,d6,d5,d4,d3,d2,dK,dQ,hJ]

num_of_cards = 52
user_sum = 0
opponent_sum = 0

#value = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'K':10,'Q':10,'J':10}

index = random.randint(0,num_of_cards)



def check_sum(index,sum):
    
    global deck
    
    if deck[index] == cA or deck[index] == sA or deck[index] == hA or deck[index] == dA:
        sum = sum + 1
        
    elif deck[index] == c2 or deck[index] == s2 or deck[index] == h2 or deck[index] == d2:
        sum = sum + 2
    
    elif deck[index] == c3 or deck[index] == s3 or deck[index] == h3 or deck[index] == d3:
        sum = sum + 3
    
    elif deck[index] == c4 or deck[index] == s4 or deck[index] == h4 or deck[index] == d4:
        sum = sum + 4
    
    elif deck[index] == c5 or deck[index] == s5 or deck[index] == h5 or deck[index] == d5:
        sum = sum + 5
    
    elif deck[index] == c6 or deck[index] == s6 or deck[index] == h6 or deck[index] == d6:
        sum = sum + 6
    
    elif deck[index] == c7 or deck[index] == s7 or deck[index] == h7 or deck[index] == d7:
        sum = sum + 7
    
    elif deck[index] == c8 or deck[index] == s8 or deck[index] == h8 or deck[index] == d8:
        sum = sum + 8
    
    elif deck[index] == c9 or deck[index] == s9 or deck[index] == h9 or deck[index] == d9:
        sum = sum + 9
    
    else:
    	sum = sum + 10 
    
    return sum
    
def play_button_touch_up_inside(sender):
    
    
    global deck
    global user_sum
    global num_of_cards
    
    #user's cards
    index = random.randint(0,num_of_cards)
    view['user_card_1_imageview'].image = deck[index]
    user_sum = check_sum(index,user_sum)
    del deck[index]
    num_of_cards = num_of_cards - 1
    
    index = random.randint(0,num_of_cards)
    view['user_card_2_imageview'].image = deck[index]
    user_sum = check_sum(index,user_sum)
    del deck[index]
    num_of_cards = num_of_cards - 1
    
    view['user_total_label'].text = 'Your total = ' + str(user_sum)
    
    #dealer's cards
    dealer_card_1_image = ui.Image.named('card:BackBlue4')
    view['dealer_card_1_imageview'].image = dealer_card_1_image
    
    dealer_card_2_image = ui.Image.named('card:BackBlue4')
    view['dealer_card_2_imageview'].image = dealer_card_2_image
    
    dealer_card_3_image = ui.Image.named('card:BackBlue4')
    view['dealer_card_3_imageview'].image = dealer_card_3_image
    
    
def add_button_touch_up_inside(sender):
    
    
    global deck
    global user_sum
    global num_of_cards
    
    
    index = random.randint(0,num_of_cards)
    view['user_card_3_imageview'].image = deck[index]
    user_sum = check_sum(index,user_sum)
    del deck[index]
    num_of_cards = num_of_cards - 1
    
    view['user_total_label'].text = 'Your total = ' + str(user_sum)
    
def reveal_button_touch_up_inside(sender):
    
    global deck
    global opponent_sum
    global num_of_cards
    global user_sum
    
    index = random.randint(0,num_of_cards)
    view['dealer_card_1_imageview'].image = deck[index]
    opponent_sum = check_sum(index,opponent_sum)
    del deck[index]
    num_of_cards = num_of_cards - 1
    
    index = random.randint(0,num_of_cards)
    view['dealer_card_2_imageview'].image = deck[index]
    opponent_sum = check_sum(index,opponent_sum)
    del deck[index]
    num_of_cards = num_of_cards - 1
    
    index = random.randint(0,num_of_cards)
    view['dealer_card_3_imageview'].image = deck[index]
    opponent_sum = check_sum(index,opponent_sum)
    del deck[index]
    num_of_cards = num_of_cards - 1
    
    view['opponent_total_label'].text = 'Dealer\'s total = ' + str(opponent_sum)
    
    if user_sum > 21 and opponent_sum > 21:
        view['answer_label'].text = 'You tie'
    elif user_sum == opponent_sum:
        view['answer_label'].text = 'You tie'
    elif user_sum == 21:
        view['answer_label'].text = 'You win'
    elif opponent_sum == 21:
        view['answer_label'].text = 'You lose'
    elif user_sum > 21:
        view['answer_label'].text = 'You lose'
    elif opponent_sum > 21:
        view['answer_label'].text = 'You win'
    elif user_sum < opponent_sum:
        view['answer_label'].text = 'You lose'
    elif user_sum > opponent_sum:
        view['answer_label'].text = 'You win'
    

view = ui.load_view()
view.present('fullscreen')
