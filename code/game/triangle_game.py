"""
A small script that finds the solution to the cracker barrel peg game / triangle game.
Instructions along with one of the game's solution can be found here:
http://www.joenord.com/puzzles/peggame/
The solution is determined by building a game tree and using a depth-first search algorithm.
Game Tree: https://en.wikipedia.org/wiki/Game_tree
Depth First Search: https://en.wikipedia.org/wiki/Depth-first_search
The slot's are numbered 0 - 14 in sequential order (Top to Bottom, Left to Right)
    /0\
   /1 2\
  /3 4 5\
  etc etc
Language python 2.7
"""

import copy


class Slot(object):
    """
    Represents a single slot opening of the triangle game.
    This class holds the slot number, it's possible jump
    dictionary and helper functions around maintaining slots.
    """

    def __init__(self, num, jump_dict):
        """
        :param num: slot number corresponding to jump_from
        :param jump_dict: possible jumps in the format {jump_over: jump_to}
        """
        self.num = num
        self.jump_dict = jump_dict
        self.peg = True

    def has_peg(self):
        return self.peg

    def add_peg(self):
        self.peg = True

    def remove_peg(self):
        self.peg = False


class Triangle(object):
    """
    Represents a single board of the triangle game.
    """

    def __init__(self):
        """
        Initializes the board for a new game.
        board: consists of 15 Slot() objects
        peg_count: A running total of the slots that still contain a peg
        """
        self.board = [Slot(0, {1: 3, 2: 5}),
                      Slot(1, {3: 6, 4: 8}),
                      Slot(2, {4: 7, 5: 9}),
                      Slot(3, {4: 5, 1: 0, 6: 10, 7: 12}),
                      Slot(4, {7: 11, 8: 13}),
                      Slot(5, {2: 0, 4: 3, 8: 12, 9: 14}),
                      Slot(6, {3: 1, 7: 8}),
                      Slot(7, {4: 2, 8: 9}),
                      Slot(8, {4: 1, 7: 6, }),
                      Slot(9, {5: 2, 8: 7}),
                      Slot(10, {6: 3, 11: 12}),
                      Slot(11, {7: 4, 12: 13}),
                      Slot(12, {11: 10, 7: 3, 8: 5, 13: 14}),
                      Slot(13, {12: 11, 8: 4}),
                      Slot(14, {13: 12, 9: 5})]

        self.peg_count = 15

    def jump(self, jump_from, jump_over, jump_to):
        """Executes a jump action
        :param jump_from: Peg number.  This is the jump_from
        :param jump_over: Peg number to be jumped over and removed
        :param jump_to: Empty slot number for the peg to jump into
        """
        assert self.board[jump_from].has_peg()
        assert self.board[jump_over].has_peg()
        assert not self.board[jump_to].has_peg()
        self.peg_count -= 1
        self.board[jump_from].remove_peg()
        self.board[jump_over].remove_peg()
        self.board[jump_to].add_peg()

    def remove_first_peg(self, slot):
        """
        The first action of every game is to remove a peg from a full board
        """
        assert self.peg_count == 15
        self.peg_count -= 1
        self.board[slot].remove_peg()

    def possible_peg_jumps(self, slot):
        """Determines all possible jumps given a particular slot
        :param slot: Integer for a particular slot
        :return: Dictionary of possible jumps in the form of {jump_over: jump_to}
        """
        assert self.board[slot].has_peg()
        possible_jump_dict = {}
        for jump_over in self.board[slot].jump_dict:
            jump_to = self.board[slot].jump_dict[jump_over]
            if self.board[jump_over].has_peg() and not self.board[jump_to].has_peg():
                possible_jump_dict[jump_over] = jump_to
        return possible_jump_dict

    def all_possible_jumps(self):
        """ Determine all possible jumps for the entire board
        :return: Dictionary of Dictionaries containing slot numbers and their available jumps
        """
        output = {}
        for i in range(15):
            if self.board[i].has_peg():
                possible_jumps = self.possible_peg_jumps(i)
                if possible_jumps:
                    output[i] = possible_jumps
        return output


class GameNode(object):
    """
    Represents a single node of the game tree
    """

    def __init__(self, parent, jump, triangle):
        """
        children: Dictionary containing a jump sequence as keys and child nodes as values.
                  In the form of {(jump_from, jump_over, jump_to): GameNode()}
                  Values of the children dict that are set to None represent unexplored branches.
        :param parent: GameNode() object containing the parent node.
                       A value of None represents the root Node.
        :param jump: tuple containing the jump sequence at this node
        :param triangle: Triangle() object
        """

        # Determine whether this node is the first move of the game and act appropriately
        if isinstance(jump, (int, long)):
            triangle.remove_first_peg(jump)
        else:
            triangle.jump(*jump)

        # Fill children dictionary with all possible jump tuples as keys
        self.children = {}
        all_jumps = triangle.all_possible_jumps()
        for jump_from, jumps in all_jumps.iteritems():
            for jump_over, jump_to in jumps.iteritems():
                self.children[(jump_from, jump_over, jump_to)] = None

        self.parent = parent
        self.jump = jump
        self.triangle = triangle

    def next_node(self):
        """ Either returns a newly created child node or the current node's parent.
            Parent node is only returned if all child nodes have been analyzed
            :return: next GameNode() instance to explore
        """
        for jump, child_node in self.children.iteritems():
            if not child_node:
                return self.init_child_node(jump)
        return self.parent

    def init_child_node(self, jump):
        """Initializes a child node with it's own separate instance of Triangle()
        :param jump: The jump for the child node's triangle
                     in the form of a tuple (jump_from, jump_over, jump_to)
        :return: Newly created child node
        """
        triangle_copy = copy.deepcopy(self.triangle)
        node = GameNode(parent=self, jump=jump, triangle=triangle_copy)
        self.children[jump] = node
        return node


def jump_history(node):
    """Returns a list of moves from the start of the game to the passed in node
    :param node: GameNode() object
    :return: Move history list in chronological order
    """
    history = []
    while True:
        history.append(node.jump)
        if not node.parent:
            break
        node = node.parent
    return history[::-1]


def main():
    """
    Outputs the solution for a triangle starting with the middle peg removed
    """
    game_node = GameNode(None, 4, Triangle())
    while game_node.triangle.peg_count != 1:
        game_node = game_node.next_node()
    print jump_history(game_node)


if __name__ == "__main__":
    main()
