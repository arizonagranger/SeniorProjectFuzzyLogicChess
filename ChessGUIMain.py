import pygame as p
import sys
import os
import threading

import GUI.UI_Utils as utils
# import chessAI
#import Engine

IMG_DIR = "GUI\\Chess Pieces\\"

WIDTH = 800
HEIGHT = 800
DIMENSION = 8
screen = p.display.set_mode((int(WIDTH), HEIGHT))

SQ_SIZE = HEIGHT // DIMENSION
darkwood = p.Color(184, 139, 74)
lightwood = p.Color(227, 193, 111)

running = False
server_response = True
piece_selected = ""

tiles = []
pieces = []

#Game Properties

#If we are doing the game from this file then
#this would be a good spot to initialize


#Images loaded for the board
def loadImages():
    r = 0
    for row in pieces:
        c = 0
        for piece in row:
            directory = os.path.join(os.getcwd(), IMG_DIR + utils.get_image(piece) + ".png")
            if os.path.exists(directory):
                color = p.Color("blue")
                p.draw.rect(screen, color, p.Rect(c * SQ_SIZE + 2, r * SQ_SIZE + 2, SQ_SIZE - 4, SQ_SIZE - 4))
                img = p.image.load(directory)
                img = p.transform.scale(img, (SQ_SIZE - 8, SQ_SIZE - 8))
                screen.blit(img, (c * SQ_SIZE + 4, r * SQ_SIZE + 4))
            c += 1
        r += 1


#Backend initialization
#Game state, moves, corps for pieces, etc.


#Functions for gameplay
def chessStart():
    global pieces, running

    attack_array = []
    valid_array = []

    pieces = utils.parse_board_state()

    #variables for logging clicks
    spaceSel = () # number of spaces or squares selected
    playerClicks = []  #tracks players clicks

    #condiditon for if game is running or if pieces have been captured
    running = True

    # drawGameState(screen, valid_array, attack_array, spaceSel)
    p.display.flip()

#function to draw the board


#Screen loaction on the right of the board


#function for drawing a grid on the board
def drawBoard(screen):
    screen.fill(p.Color("white"))
    colors = [lightwood, darkwood]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            rect = p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            tiles.append(rect)


def main():
    server_thread = threading.Thread(target=utils.check_server)
    server_thread.start()

    if utils.server_response:
        p.init()
        p.display.set_caption('Chess AI Project')

        chessStart()
        drawBoard(screen)
        p.display.flip()

        while running and utils.server_response:
            # load images
            loadImages()

            for event in p.event.get():
                if event.type == p.MOUSEBUTTONDOWN:
                    pos = p.mouse.get_pos()
                    selected_tile = [o for o in tiles if o.collidepoint(pos)]

                    if len(selected_tile) != 0:
                        print("Tile: " + str(int(selected_tile[0].y / SQ_SIZE)) + ", " + str(int(selected_tile[0].x / SQ_SIZE)))
                        print(pieces[int(selected_tile[0].y / SQ_SIZE)][int(selected_tile[0].x / SQ_SIZE)])
                p.display.update()

        p.quit()


if __name__ == "__main__":
    main()