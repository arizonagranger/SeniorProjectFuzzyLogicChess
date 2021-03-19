# written by Haley Granger
# Senior Project AI Chess


##########################anytime you see multiple of these it means we need stuff from the rules engine#######################
# import AI Rules Engine
# How do i do this? IDK
##%3E
#Example requests:
#POST http://localhost:4850/act?action-str=e2%3Ee3
#GET http://localhost:4850/new-game
#POST http://localhost:4850/end-turn
#GET http://localhost:4850/actions-for?coord=e2

# import GUI and other important functionalities of the project

# King Script

import requests
URL = "http://localhost:4850/new-game"

r = requests.get(url = URL)
"""""
isThreat = False
# pieces Dict shows initial pieces of board, change as coordinates are called
# _r indicates right side as seen from eyes of AI looking at board (f-h)
# _l indicates left side as seen from eyes of AI looking at board (a-c)
# pawn numbering begins on left side and increases (P8 is on h2 starting)
###############this is a placeholder dict until we get rules engine, need to know format and how to import currentboard variable ##########
piecesDict = {
    "K": "e1",
    "Q": "d1",
    "P_r": "f1",
    "P_l": "c1",
    "N_r": "g1",
    "N_l": "b1",
    "A_r": "h1",
    "A_l": "a1",
    "I1": "a2",
    "I2": "b2",
    "I3": "c2",
    "I4": "d2",
    "I5": "e2",
    "I6": "f2",
    "I7": "g2",
    "I8": "h2"
}

################# currentboard from rules engine (save-state?) ##################################
# calls king_scanthreats
# returns possible immediate moves in an array

def king_scanboard(currentboard):
    ##### updates coordinates in piecesDict for currentboard #######
    for x in piecesDict:
        ################### currentboard must be able to access individual piece coordinates ##############
        piecesDict[x] = currentboard.x
    if king_scanthreats():
        



# scans board for current threats and looks for future threats
# returns true for current threats and an array of future threats up to x moves
def king_scanthreats():

    return isThreat

# iterates through the moves for a specific piece
# assigns values for that move and returns the best move for that piece
def evaluate_pieces(coord):
    ######### iterate through moves-for(coord) #####################
"""
print(r)