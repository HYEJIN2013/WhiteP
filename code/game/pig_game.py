import random
import time
import pickle
import threading
import queue
from tkinter import *
from PIL import Image, ImageTk

LARGE_FONT = ("Tahoma", 18)
MEDIUM_FONT = ("Menlo", 15)
SMALL_FONT = ("Menlo", 12)


def input_action():
    while True:
        try:
            action = input("Roll or hold (r=roll, h=hold): ")
            if action == 'r' or action == 'h':
                return action
            else:
                raise ValueError

        except ValueError:
            print('You need to enter r or h')
            continue


class Die:
    """A die to play with."""

    def __init__(self):
        self.value = random.randint(1, 6)

    def roll(self):
        """Returns the rolled dice, or raises RolledOneException if 1."""

        self.value = random.randint(1, 6)
        print('--> {}'.format(self.value))

        return self.value

    def __str__(self):
        return "--> " + str(self.value) + "."


class Box:
    """Temporary score box holder class."""

    def __init__(self):
        self.value = 0

    def reset(self):
        self.value = 0

    def add_dice_value(self, dice_value):
        self.value += dice_value


class Player(object):
    """Base class for different player types."""

    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self, round_score):
        """Adds player_score to total score."""
        self.score += round_score

    def __str__(self):
        """Returns player name and current score."""
        return str(self.name) + ": " + str(self.score)


class ComputerPlayer(Player):
    def __init__(self):
        f = open("cpu.txt", "rb")
        self.cpu = pickle.load(f)
        f.close()
        super(ComputerPlayer, self).__init__("ME")

    def keep_rolling(self, opponent_score, turn_score):
        """Randomly decides if the CPU player will keep rolling."""
        return self.cpu[self.score][opponent_score][turn_score]


class HumanPlayer(Player):
    def __init__(self, name):
        super(HumanPlayer, self).__init__(name)

    def keep_rolling(self):
        """Asks the human player, if they want to keep rolling."""

        human_decision = input_action()
        if human_decision == 'r':
            return True
        else:
            return False


def show_instruction():
    """Prints rules of the game."""

    rules = ""

    f = open('game_rules.txt', 'r')
    for line in f:
        rules += line
    f.close()

    return rules


class GameManager:
    def __init__(self):
        """Initialises the game, optionally asking for human player names."""

        self.players = []

        self.players.append(HumanPlayer("YOU"))
        self.players.append(ComputerPlayer())

        self.no_of_players = 2

        self.current_player = 0

        self.die = Die()
        self.box = Box()

    @staticmethod
    def show_instruction():
        """Prints rules of the game."""

        rules = ""

        f = open('game_rules.txt', 'r')
        for line in f:
            rules += line + "\n"
        f.close()

        return rules

    def next_player(self):
        """Advanced self.current_player to next player."""
        self.current_player = (self.current_player + 1) % self.no_of_players

    def get_all_scores(self):
        """Returns a join all players scores."""
        return ', '.join(str(player) for player in self.players)

    def is_human(self):
        if self.current_player == 0:
            return True
        return False

    def play_game(self):
        """Plays an entire game."""

        print(self.show_instruction())

        while all(player.score < 100 for player in self.players):
            print('\nCurrent score --> {}'.format(self.get_all_scores()))
            print('\n*** {} to play ***'.format(self.players[self.current_player].name))
            self.box.reset()

            while self.keep_rolling():
                pass

            self.players[self.current_player].add_score(self.box.value)
            self.next_player()

        # The other player has won...
        self.next_player()
        print(' {} has won '.format(self.players[self.current_player].name).center(70, '*'))

    def keep_rolling(self):
        """Adds rolled dice to box. Returns if human/cpu wants to continue.
        If either player rolls a 1, the box value is reset, and turn ends.
        """

        if self.is_human():
            decision = self.players[self.current_player].keep_rolling()
        else:
            decision = self.players[self.current_player].keep_rolling(self.players[0].score, self.box.value)

        if decision:
            val = self.die.roll()
            if val != 1:
                self.box.add_dice_value(val)
                print('Current sum: {}'.format(self.box.value))

                # Check if human (by asking) or computer(calculating) will keep rolling
                return decision
            else:
                print('{} rolled 1: lost all points at this round.'.format(self.players[self.current_player].name))
                self.box.reset()
                return False


class GUI:
    def __init__(self, master, queue_list, action_command):

        self.die_queue = queue_list[0]
        self.box_queue = queue_list[1]
        self.score_queue = queue_list[2]

        # Define some constants
        self.ROLL = 1
        self.HOLD = 2
        self.END = 3

        BG = '#DDDCDA'

        self.player_name = ["You", "I"]
        self.player_turn = ["YOUR", "MY"]
        self.current_player = 0

        container = Frame(master)
        container.pack(side="top", fill="both", expand=True)

        for row in range(1):
            container.grid_rowconfigure(row, weight=1)
        for column in range(4):
            container.grid_columnconfigure(column, weight=1)

        # Instruction Frame
        instruction_frame = Frame(container, bg=BG)
        for row in range(5):
            instruction_frame.grid_rowconfigure(row, weight=1)
        for column in range(1):
            instruction_frame.grid_columnconfigure(column, weight=1)
        instruction_frame.grid(row=0, column=0, ipady=5, ipadx=5, sticky="nsew")

        rules_label = Label(instruction_frame, text="Rules of the game", font=LARGE_FONT, fg='red', bg=BG)
        rules_label.grid(row=1, ipady=5, ipadx=5, sticky="nsew")

        rules = show_instruction()
        rules_content = Label(instruction_frame, text=rules, font=SMALL_FONT, justify=LEFT, wraplength=300, bg=BG)
        rules_content.grid(row=2, ipady=5, ipadx=5, sticky="nsew")

        # Play Frame
        play_frame = Frame(container, bg=BG)
        play_frame.grid(row=0, column=1, columnspan=3, ipady=5, ipadx=5, sticky="nsew")

        for row in range(8):
            play_frame.grid_rowconfigure(row, weight=1)
        for column in range(1):
            play_frame.grid_columnconfigure(column, weight=1)

        # Score board Frame
        self.score_board = LabelFrame(play_frame, bg=BG)
        self.score_board.grid(row=0, ipadx=5, ipady=5, padx=10, pady=5, sticky="nsew")

        for row in range(5):
            self.score_board.grid_rowconfigure(row, weight=1)
        for column in range(2):
            self.score_board.grid_columnconfigure(column, weight=1)

        score_label = Label(self.score_board, text="Scoreboard", font=LARGE_FONT, fg='darkgreen', bg=BG)
        score_label.grid(row=0, columnspan=2, sticky="nsew")

        self.player_score = Label(self.score_board, text="0", font=MEDIUM_FONT, bg=BG)
        self.player_score.grid(row=1, column=0, sticky="nsew")

        player_label = Label(self.score_board, text="YOU", font=MEDIUM_FONT, bg=BG)
        player_label.grid(row=2, column=0, sticky="nsew")

        self.computer_score = Label(self.score_board, text="0", font=MEDIUM_FONT, bg=BG)
        self.computer_score.grid(row=1, column=1, sticky="nsew")

        computer_label = Label(self.score_board, text="COMPUTER", font=MEDIUM_FONT, bg=BG)
        computer_label.grid(row=2, column=1, sticky="nsew")

        turn_point_label = Label(self.score_board, text="TURN POINTS", font=MEDIUM_FONT, bg=BG)
        turn_point_label.grid(row=3, columnspan=2, sticky="nsew")

        self.turn_point = Label(self.score_board, text="0", font=MEDIUM_FONT, bg=BG)
        self.turn_point.grid(row=4, columnspan=2, sticky="nsew")

        # Turn board Frame
        self.turn_board = LabelFrame(play_frame, bg=BG)
        self.turn_board.grid(row=1, rowspan=7, ipadx=5, ipady=5, padx=10, pady=5, sticky="nsew")

        for row in range(5):
            self.turn_board.grid_rowconfigure(row, weight=1)
        for column in range(2):
            self.turn_board.grid_columnconfigure(column, weight=1)

        self.turn_label = Label(self.turn_board, text="YOUR TURN", font=LARGE_FONT, fg='blue', bg=BG)
        self.turn_label.grid(row=0, columnspan=2, ipady=5, ipadx=5, sticky="nsew")

        self.noti = Label(self.turn_board, text="You rolled 1, all turn points gone.", wraplength=280, font=SMALL_FONT, bg=BG)
        self.noti.grid(row=1, columnspan=2, sticky="nsew")

        self.die_image = Label(self.turn_board, bg=BG)
        self.update_die(1)
        self.die_image.grid(row=2, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.roll_btn = Button(self.turn_board, text="Roll", font=MEDIUM_FONT, highlightbackground=BG,
                               command=lambda: action_command(self.ROLL))
        self.roll_btn.grid(row=3, rowspan=2, column=0, ipadx=10, ipady=10, sticky="nsew")

        self.hold_btn = Button(self.turn_board, text="Hold", font=MEDIUM_FONT, highlightbackground=BG,
                               command=lambda: action_command(self.HOLD))
        self.hold_btn.grid(row=3, rowspan=2, column=1, ipadx=10, ipady=10, sticky="nsew")

        self.reset_game()

    def update_die(self, val):
        size = 100, 100
        img = Image.open("die_sides/{}.jpg".format(val))
        img.thumbnail(size)
        die_img = ImageTk.PhotoImage(img)
        self.die_image.config(image=die_img)
        self.die_image.image = die_img

    def update_turn_point(self, value):
        self.turn_point.config(text="{}".format(value))

    def update_player_score(self, score):
        self.player_score.config(text=score)

    def update_computer_score(self, score):
        self.computer_score.config(text=score)

    def update_noti(self, text):
        self.noti.config(text=text)

    def update_turn(self, text):
        self.turn_label.config(text=text)

    def reset_game(self):
        self.update_player_score(0)
        self.update_computer_score(0)
        self.update_turn_point(0)
        self.update_turn("YOUR TURN")
        self.update_noti("Roll or hold?")
        self.update_die(1)

    def change_player(self):
        self.current_player = (self.current_player + 1) % 2

    def disable_buttons(self):
        self.roll_btn.config(state=DISABLED)
        self.hold_btn.config(state=DISABLED)

    def active_buttons(self):
        self.roll_btn.config(state=ACTIVE)
        self.hold_btn.config(state=ACTIVE)

    def update_incoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.box_queue.qsize():
            try:
                self.update_turn_point(self.box_queue.get(0))
            except queue.Empty:
                pass

        while self.score_queue.qsize():
            try:
                score = self.score_queue.get(0)

                if self.current_player == 0:
                    self.update_player_score(score)
                else:
                    self.update_computer_score(score)
            except queue.Empty:
                pass

        while self.die_queue.qsize():
            try:
                die_side = self.die_queue.get(0)
                self.update_die(die_side)

                if die_side != 1:
                    self.update_noti("Rolled {}\nRoll or hold?".format(die_side))
                    self.update_turn_point(self.box_queue.get(0))
                elif die_side == 1:
                    self.update_noti("Rolled 1. Lost all turn points.")
                    self.update_turn_point(self.box_queue.get(0))
                    self.update_turn("{} TURN!!".format(self.player_turn[self.current_player]))
                    self.update_noti("")

                    if self.current_player == 0:
                        self.disable_buttons()
                    else:
                        self.active_buttons()

                    self.change_player()
                elif die_side == 0:
                    # means hold
                    self.update_noti("Hold")
                    self.turn_label.after(2000,
                                          self.update_turn("{} TURN!!".format(self.player_turn[self.current_player])))

                    print(self.score_queue)

                    while self.score_queue.qsize() < 1:
                            pass

                    if self.current_player == 0:
                        self.update_player_score(self.score_queue.get(0))
                    else:
                        self.update_computer_score(self.score_queue.get(0))

                    self.update_turn_point(self.box_queue.get(0))

                    if self.current_player == 0:
                        self.disable_buttons()
                    else:
                        self.active_buttons()

                    self.change_player()
            except queue.Empty:
                pass


class EndGameGUI(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="Game over")
        label.grid(row=0, sticky="nsew")

        play_again = Button(self, text="Play again", font=SMALL_FONT, command='')# lambda : controller.show_frame(PlayGUI))
        play_again.grid(row=1, ipadx=5, ipady=5, padx=10, sticky="nsew")


class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """

    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """

        self.master = master

        # Create the queue
        self.die_queue = queue.Queue()
        self.box_queue = queue.Queue()
        self.score_queue = queue.Queue()

        queue_list = [self.die_queue, self.box_queue, self.score_queue]

        self.action_queue = queue.Queue()

        # Set up the GUI part
        self.gui = GUI(master, queue_list, self.action_command)

        # Define some constants
        self.ROLL = 1
        self.HOLD = 2
        self.RESET = 3
        self.END = 4

        # Game init
        self.no_of_players = 2

        self.players = []
        self.players.append(HumanPlayer("YOU"))
        self.players.append(ComputerPlayer())

        self.current_player = 0

        self.die = Die()
        self.box = Box()

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = True
        self.thread = threading.Thread(target=self.game_thread)
        self.thread.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.async_call()

    def reset_game(self):
        self.no_of_players = 2

        self.players = []
        self.players.append(HumanPlayer("YOU"))
        self.players.append(ComputerPlayer())

        self.current_player = 0

        self.die = Die()
        self.box = Box()

        # update scoreboard
        # update die

    def next_player(self):
        self.current_player = (self.current_player + 1) % self.no_of_players

    def get_player_score(self):
        return self.players[self.current_player].score

    """
    def roll_action(self):
        val = self.die.roll()
        self.die_queue.put(val)
        if val != 1:
            self.box.add_dice_value(val)
            self.box_queue.put(self.box.value)
        else:
            self.box.reset()
            self.box_queue.put(self.box.value)
            if self.current_player == 0:
                # self.update_noti("MY TURN :D")
                # self.hide_btns()
                self.next_player()
                self.computer_decision()
            else:
                # self.update_noti("YOUR TURN!!")
                # self.show_btns()
                self.next_player()
    def hold_action(self):
        self.players[self.current_player].add_score(self.box.value)
        self.box.reset()
        self.box_queue.put(self.box.value)
        if self.current_player == 0:
            self.player_score_queue.put(self.get_player_score())
            # self.update_noti("MY TURN :D")
            # self.hide_btns()
            # self.check_winner()
            self.next_player()
            self.computer_decision()
        else:
            self.computer_score_queue.put(self.get_player_score())
            # self.show_btns()
            # self.update_noti("YOUR TURN!!")
            # self.check_winner()
            self.next_player()
    def computer_decision(self):
        if self.current_player == 1:
            if self.players[self.current_player].keep_rolling(self.players[0].score, self.box.value):
                self.roll_action()
                time.sleep(2000)
                self.computer_decision()
            else:
                self.hold_action()
    """

    def async_call(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.update_incoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(200, self.async_call)

    def game_thread(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """
        while self.running:

            while all(player.score < 100 for player in self.players):
                print('\nCurrent score --> {}'.format(', '.join(str(player) for player in self.players)))
                print("Turn of " + self.players[self.current_player].name)
                self.box.reset()

                while self.keep_rolling():
                    if self.current_player == 1:
                        time.sleep(2)
                    pass

                print("Hold")
                self.players[self.current_player].add_score(self.box.value)

                self.score_queue.put(self.get_player_score())

                self.box_queue.put(self.box.value)

                self.next_player()

            # The other player has won...
            self.next_player()

    def keep_rolling(self):
        """Adds rolled dice to box. Returns if human/cpu wants to continue.
        If either player rolls a 1, the box value is reset, and turn ends.
        """

        if self.current_player == 0:
            while self.action_queue.qsize() < 1:
                pass
            decision = self.action_queue.get(0)
        else:
            decision = self.players[self.current_player].keep_rolling(self.players[0].score, self.box.value)

        if decision:
            print("Roll")
            val = self.die.roll()
            self.die_queue.put(val)

            if val != 1:
                self.box.add_dice_value(val)
                self.box_queue.put(self.box.value)
                print("Turn point: {}".format(self.box.value))
                # Check if human (by asking) or computer(calculating) will keep rolling
                return decision
            else:
                print('{} rolled 1: lost all points at this round.'.format(self.players[self.current_player].name))
                self.box.reset()
                self.box_queue.put(self.box.value)
                return False

    def action_command(self, action):
        if action == self.ROLL:
            self.action_queue.put(True)
        elif action == self.HOLD:
            self.action_queue.put(False)
        elif action == self.RESET:
            self.reset_game()
        elif action == self.END:
            self.running = False

    def exit_app(self):
        self.master.destroy()
        sys.exit(1)


def main():
    app_gui = Tk()
    app_gui.wm_title("Die game")
    app_gui.geometry("680x500")

    player = ThreadedClient(app_gui)

    app_gui.mainloop()
    # app_gui.protocol("WM_DELETE_WINDOW", player.exit_app())

if __name__ == '__main__':
    main()
