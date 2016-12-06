"""Shockwave is a simple game in which the objective is to make all the tiles the same color."""

import sys
import random
import pygame

# miscellaneous constants
NAME = "Shockwave"

# color constants
DEFTILECOLOR = (16,178,232)
FLIPTILECOLOR = (70,232,16)
BGCOLOR = (0,0,0)

# size-related constants
GRIDH = 5
GRIDW = 5
XMARGIN = 40
YMARGIN = 40
XTILEGAP = 2
YTILEGAP = 2
TILEWIDTH = 30
TILEHEIGHT = 30
# centers grid in window
WINW = ((XMARGIN * 2) + ((TILEWIDTH + XTILEGAP) * GRIDW))
WINH = ((YMARGIN * 2) + ((TILEHEIGHT + YTILEGAP) * GRIDH))

class Tile():
    """Represents the colored squares in the game."""

    def __init__(self,gridrow,gridcol):
        self.colored = False
        self.height = TILEHEIGHT
        self.width = TILEWIDTH
        self.rect = None
        self.gridrow = gridrow
        self.gridcol = gridcol

class Grid():
    """Represents the grid of tiles in the game."""

    def __init__(self,grid):
        self.grid = grid
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def flip_tile(self,tile):
        tile.colored = not tile.colored

    def flip_row(self, row):
        for tile in self.grid[row]:
            self.flip_tile(tile)
                     
    def flip_column(self, column):
        for row in self.grid:
            self.flip_tile(row[column])
    
    def randomize_tiles(self):
        for row in self.grid:
            for tile in row:
                if random.randint(0,1) == 1:
                    self.flip_row(tile.gridrow)
                    self.flip_column(tile.gridcol)
	
    def assign_rects(self):
        basex = 0
        basey = 0
        for row in self.grid:
            for tile in row:
                tile.rect = pygame.Rect(basex + XMARGIN,basey + YMARGIN,
           tile.width,tile.height)
                basex += (XTILEGAP + tile.width)
            basex = 0
            basey += (YTILEGAP + tile.height)
      
    def draw_grid(self,surface):
        """Draws Tiles to a surface from a Grid object."""
        for row in self.grid:
            for tile in row:
                pygame.draw.rect(surface,DEFTILECOLOR,tile.rect)

def create_grid(width,height):
    """Creates multidimensional array of Tile objects."""
    fullG = []
    # Used for incrementing.
    r = 0
    c = 0
    for row in range(height):
        row = []
        for column in range(width):
            row.append(Tile(r,c))
            c += 1
        c = 0
        fullG.append(row)
        r += 1
    return Grid(fullG)

def tile_at_location(grid,coords):
    """Checks if a tile is at a given coordinate."""
    for row in grid.grid:
        for tile in row:
            if tile.rect.collidepoint(coords[0],coords[1]):
                return tile
    return False
