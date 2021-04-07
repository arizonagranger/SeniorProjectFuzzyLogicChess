import pygame as p
import sys
import os
import threading

import GUI.UI_Utils as utils
# import chessAI
#import Engine

IMG_DIR = "GUI\\Chess Pieces\\"

WIDTH = 1200
HEIGHT = 800
DIMENSION = 8
screen = p.display.set_mode((int(WIDTH), HEIGHT))

SQ_SIZE = HEIGHT // DIMENSION
darkwood = p.Color(184, 139, 74)
lightwood = p.Color(227, 193, 111)

running = False
server_response = True

tiles = []
pieces = []
selected_piece = []
buttons = []
action_queue = []

#Game Properties

#If we are doing the game from this file then
#this would be a good spot to initialize


#Images loaded for the board
def loadImages():
    r = DIMENSION - 1
    for row in pieces:
        c = DIMENSION - 1
        for piece in row:
            directory = os.path.join(os.getcwd(), IMG_DIR + utils.get_image(piece) + ".png")
            if os.path.exists(directory):
                color = p.Color(utils.get_piece_delegation(pieces, r, c))
                p.draw.rect(screen, color, p.Rect(c * SQ_SIZE + 2, r * SQ_SIZE + 2, SQ_SIZE - 4, SQ_SIZE - 4))
                img = p.image.load(directory)
                img = p.transform.scale(img, (SQ_SIZE - 8, SQ_SIZE - 8))
                screen.blit(img, (c * SQ_SIZE + 4, r * SQ_SIZE + 4))
            c -= 1
        r -= 1


#Backend initialization
#Game state, moves, corps for pieces, etc.


#Functions for gameplay
def chessStart():
    global pieces, running

    pieces = utils.parse_board_state()
    drawBoard(screen)
    setupButtons()

    attack_array = []
    valid_array = []

    #variables for logging clicks
    spaceSel = () # number of spaces or squares selected
    playerClicks = []  #tracks players clicks

    #condition for if game is running or if pieces have been captured
    running = True

    # drawGameState(screen, valid_array, attack_array, spaceSel)
    p.display.flip()


#Setup for the buttons
def setupButtons():
    AddButton(890, 360, 150, 60, "Move", p.Color("lightsalmon"), p.Color("grey"), submitMoves)
    AddButton(890, 130, 150, 60, "Quit", p.Color("lightsalmon"), p.Color("grey"), quit)


# Helper method to create buttons
def AddButton(x, y, w, h, text, color, selectColor, action):
    b = utils.Button(x, y, w, h, text, color, selectColor, action)

    b.rect = p.draw.rect(screen, b.color, [b.x, b.y, b.w, b.h])
    textFont = p.font.SysFont("Calibri", 32)
    textObj = textFont.render(b.text, True, p.Color("black"))
    textSize = textObj.get_size()
    screen.blit(textObj, (b.x + b.w / 2 - textSize[0] / 2, b.y + b.h / 2 - textSize[1] / 2))
    buttons.append(b)


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

    # load images
    loadImages()


def clickEvent():
    pos = p.mouse.get_pos()
    selected_tile = [o for o in tiles if o.collidepoint(pos)]
    selected_button = [b for b in buttons if b.rect.collidepoint(pos)]

    if len(selected_tile) != 0:
        coords = [int(selected_tile[0].x / SQ_SIZE), DIMENSION - int(selected_tile[0].y / SQ_SIZE) - 1]
        doAction(coords)

    if len(selected_button) != 0:
        selected_button[0].action()


# Request move from RulesEngine
def doAction(coords):
    global selected_piece

    # Check if piece is already selected
    if len(selected_piece) != 0:
        moves = utils.move_reader(selected_piece)
        # Check if there is a piece at new location (attack)
        if utils.get_piece(coords)[0] != "":
            # Check if position is valid
            if coords in moves:
                print("Added attack to queue")
        # Move piece to new location
        else:
            # Check if position is valid
            if coords in moves:
                print("Added move to queue")
        selected_piece = []
    # Check if tile that is clicked has a piece at coordinate
    elif utils.get_piece(coords)[0] != "":
        selected_piece = coords
    # Reset selected piece
    else:
        selected_piece = []


# Submit moves function
# Move notation:
# url = URL + "actions-for" + move

def submitMoves():
    print("Submit")
    p.display.update()
    return


#This is one of our main functions
def quit():
    print("Quit")
    sys.exit(0)

def main():
    # Create thread that checks whether the RulesEngine is connected
    server_thread = threading.Thread(target=utils.check_server)
    server_thread.start()

    if utils.server_response:
        p.init()
        p.display.set_caption('Chess AI Project')

        chessStart()

        while running and utils.server_response:
            for event in p.event.get():
                if event.type == p.MOUSEBUTTONDOWN:
                    clickEvent()
        p.quit()


if __name__ == "__main__":
    main()