from shockobjs import *
import pygame

pygame.init()

# All constants referenced are stored in the shockobjs.py file.

def main():
    # create window
    SCREEN = pygame.display.set_mode((WINW,WINH))
    pygame.display.set_caption(NAME)
    SCREEN.fill(BGCOLOR)

    # create game grid
    mainGrid = create_grid(GRIDW,GRIDH)
    mainGrid.assign_rects()
    mainGrid.draw_grid(SCREEN)

    # randomize game grid
    mainGrid.randomize_tiles()

    while True: # main loop
        clickCoords = None
        # quit if window closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                clickCoords = event.pos
        
        # Checks if there's a tile at the clicked location.
        if clickCoords is not None:
            clickedTile = tile_at_location(mainGrid,clickCoords)
            if clickedTile is not False:
                for row in mainGrid.grid:
                    for tile in row:
                        if clickedTile == tile:
                            mainGrid.flip_row(clickedTile.gridrow)
                            mainGrid.flip_column(clickedTile.gridcol)
        
        # Updates colors of tiles in board.
        for row in mainGrid.grid:
            for tile in row:
                if tile.colored:
                    SCREEN.fill(FLIPTILECOLOR,rect=tile.rect)
                else:
                    SCREEN.fill(DEFTILECOLOR,rect=tile.rect)

        pygame.display.update()

if __name__ == "__main__":
    main()
