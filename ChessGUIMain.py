import pygame as p
import sys

#import Engine
#import AI 

#Game Properties

#If we are doing the game from this file then
#this would be a good spot to initialize


#Images loaded for the board


#Backend initialization
#Game state, moves, corps for pieces, etc.


#Functions for gameplay
def chessStart():
    attack_array = []
    valid_array = []

    #variables for logging clicks
    spaceSel = () # number of spaces or squares selected
    playerClicks = []  #tracks players clicks

    #load images 
    running = True

    #condiditon for if game is running or if pieces have been captured


    drawGameState(screen, valid_array, attack_array, spaceSel)
    p.display.flip()

#function to draw the board


#Screen loaction on the right of the board


#function for drawing a grid on the board
def drawBoard(screen):
    screen.fill(p.Color("white"))
    colors = [p.Color("white"), p.Color("dark grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
          #  p.draw.rect(screen, color, p.Rect(c* Square size))





if __name__ == "__main__":
    main()