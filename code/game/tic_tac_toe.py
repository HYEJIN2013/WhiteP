#Helper Functions

"""
Whenever you have a large problem to solve, 
try to break it down into multiple smaller problems.
Then go about solving the smaller problems, and, if 
possible, turn each solution into its own procedure / function.
"""

############    Problem Statement     #########################
"""
Let's make a playable tick-tac-toe game using ansi characters!
"""

#Frist, let's have a variable keep status for the current positions
current_positions = {"top left": " ", "top center": " ", "top right": " ",
             "center left": " ", "center": " ", "center right": " ",
             "bottom left": " ", "bottom center": " ", "bottom right": " "}


#Let's also keep track of the current turn
player_turn = "X"

#Now, let's see if we can display the board based on current_positions:
def display_board(current_positions):
    display_string = """
    {top left}    |    {top center}   |   {top right}
         |        |                
    ---------------------
         |        |      
    {center left}    |    {center}   |   {center right}
         |        |      
    ---------------------
         |        |      
    {bottom left}    |    {bottom center}   |   {bottom right}
         |        |      
    """.format(**current_positions)
    print display_string

#print display_string
def advance_turn(player_turn):
    if player_turn == "X":
        player_turn = "O"
    else:
        player_turn = "X"
    return player_turn

#Let's get some user input for our next turn:
def make_user_move(current_positions, player_turn):
    acceptable_move = False
    while not acceptable_move:
        input_options = "Please type in where to go next!  You can select from the following options:\n"
        possible_options = []
        for position in current_positions:
            if current_positions[position] == " ":
                possible_options.append(position)
                input_options += position + "\n"
        player_move = raw_input(input_options).lower()
        if player_move in possible_options:
            acceptable_move = True
            current_positions[player_move] = player_turn
            player_turn = advance_turn(player_turn)
            return current_positions, player_turn
        else:
            print "That's not an option!"
            print input_options


# display_board(current_positions)
# current_positions, player_turn = make_user_move(current_positions, player_turn)

#Now let's make the game able to have a winner!
def get_X_and_O_locations(current_positions):
    X_positions = []
    O_positions = []
    for position in current_positions:
        if current_positions[position] == "X":
            X_positions.append(position)
        elif current_positions[position] == "O":
            O_positions.append(position)
    return X_positions, O_positions

def game_over(current_positions):
    #Limited number of winning positions, let's just list them all
    X_positions, O_positions = get_X_and_O_locations(current_positions)
    winners = [["top left", "top center", "top right"],
               ["center left", "center", "center right"],
               ["bottom left", "bottom center", "bottom right"],
               ["top left", "center left", "bottom left"],
               ["top center", "center", "bottom center"],
               ["top right", "center right", "bottom right"],
               ["top left", "center", "bottom right"],
               ["top right", "center", "bottom left"]]
    for player in [X_positions, O_positions]:
        for winner in winners:
            player_wins = True
            for position in winner:
                if position not in player:
                    player_wins = False
                    break
            if player_wins:
                display_board(current_positions)
                return current_positions[player[0]] + "wins!"
    if len(X_positions) + len(O_positions) >= 9:
        display_board(current_positions)
        return "Draw"
    else:
        return False



def play_game():
    current_positions = {"top left": " ", "top center": " ", "top right": " ",
             "center left": " ", "center": " ", "center right": " ",
             "bottom left": " ", "bottom center": " ", "bottom right": " "}
    player_turn = "X"
    result = False
    while not result:
        display_board(current_positions)
        current_positions, player_turn = make_user_move(current_positions, player_turn)
        result = game_over(current_positions)
        if result:
            print "GAME OVER"
            print "Result: ", result


play_game()
    
