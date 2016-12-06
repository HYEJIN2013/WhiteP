__author__ = 'Peter Lindberg'

import curses


class Point:
    def __init__(self, x, y, bound):
        self.x = x
        self.y = y
        self.bound = bound


class Cell:
    def __init__(self, x, y, bound=50):
        self.point = (x, y)
        self._bound = bound

    def list_neighbors(self):
        offsets = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]
        x, y = self.point
        neighbors = [[x + point[0], y + point[1]] for point in offsets]
        for neighbor in neighbors:
            for i in range(0, len(neighbor)):
                if neighbor[i] < 0:
                    neighbor[i] += self._bound
                if neighbor[i] >= self._bound:
                    neighbor[i] -= self._bound
        return neighbors

    def count_alive_neighbors(self, alive):
        alive_points = [list(x.point) for x in alive]
        alive_neighbors = [x for x in self.list_neighbors() if x in alive_points]
        return len(alive_neighbors)

    def age(self, w):
        count = self.count_alive_neighbors(w.alive_list)
        #print count,
        if count in w.birth_rules:
            w.birth(self)
        elif count not in w.stay_alive_rules:
            w.death(self)


def compare_cells(a, b):
    if a.point == b.point:
        return True
    else:
        return False


class Warden:
    def __init__(self, g=50):
        self._grid_size = g
        self.alive_list = []
        self._birth_list = []
        self._death_list = []
        self._the_grid = []
        self.birth_rules = tuple([3])
        self.stay_alive_rules = (2, 3)
        for c in [[x, y, g] for x in range(0, g) for y in range(0, g)]:
            self._the_grid.append(Cell(*c))
            # self._window = curses.initscr()
        # curses.cbreak()

    def birth(self, c):
        if c not in self.alive_list:
            # print "birth",
            # print c.point
            self._birth_list.append(c)

    def death(self, c):
        if c in self.alive_list:
            # print "added to death list",
            # print c.point
            self._death_list.append(c)

    def tic(self):
        for c in self._the_grid:
            c.age(self)
        self.alive_list = [x for x in self.alive_list if x not in self._death_list]
        self.alive_list.extend(self._birth_list)
        self._birth_list = []
        self._death_list = []

    def print_cells(self, scr):
        if len(self.alive_list) > 0:
            scr.clear()
            for cell in self.alive_list:
                x, y = cell.point
                #print cell.point,
                scr.addch(y, x, ord("#"))
            scr.refresh()
        return len(self.alive_list)

    def load_seed(self, seed):
        offset = 5
        seed_cells = [[seed[i], seed[i + 1]] for i in range(0, len(seed), 2)]
        for c in seed_cells:
            x = c[0] + offset
            y = c[1] + offset
            cell_to_find = Cell(x, y)
            for grid_cell in self._the_grid:
                if compare_cells(grid_cell, cell_to_find):
                    self.alive_list.append(grid_cell)
        print "{0} cells alive after seed load".format(len(self.alive_list))

    def __del__(self):
        print "warden deconstructor"
        curses.endwin()


def main():
    print "game of life"
    blinker = [0, 0, 0, 1, 0, 2]
    glider = [0, 2, 1, 0, 1, 2, 2, 1, 2, 2]
    spaceship = [0, 0, 0, 3, 1, 4, 2, 0, 2, 4, 3, 1, 3, 2, 3, 3, 3, 4]
    gun = [1, 5, 2, 5, 1, 6, 2, 6, 35, 3, 35, 4, 36, 3, 36, 4, 12, 4, 11, 5, 11, 6, 11, 7, 12, 8, 13, 9, 14, 9, 14, 3,
           13, 3, 16, 4, 18, 6, 15, 6, 17, 5, 17, 6, 17, 7, 16, 8, 21, 5, 21, 4, 21, 3, 22, 5, 22, 4, 22, 3, 23, 2, 23,
           6, 25, 2, 25, 1, 25, 6, 25, 7]
    gsubset = [12, 4, 11, 5, 11, 6, 11, 7, 12, 8, 13, 9, 14, 9, 14, 3, 13, 3, 16, 4, 18, 6, 15, 6, 17, 5, 17, 6, 17, 7,
               16, 8]
    diehard = [0, 0, 0, 1, 1, 0, 1, 1, 0, 5, 0, 7, 1, 6, 2, 6]
    custom = [0, 0, 0, 1, 0, 2, 1, 5, 2, 3, 2, 5, 3, 4, 3, 5]

    w = Warden()
    print "warden created"

    w.load_seed(glider)
    print "initial seed loaded"

    scr = None
    scr = curses.initscr()
    curses.cbreak()
    alive = w.print_cells(scr)
    # char = ord('n')
    #scr.addstr(0,0,"before loop")
    scr.refresh()
    scr.getch()
    while alive > 0:
        w.tic()
        alive = w.print_cells(scr)
        #char = scr.getch()
    curses.endwin()
    print "the end"


if __name__ == "__main__":
    main()
