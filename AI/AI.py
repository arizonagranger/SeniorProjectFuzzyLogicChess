# written by Haley Granger
# Senior Project AI Chess

#%3E
#Example requests:
#POST http://localhost:4850/act?action-str=e2%3Ee3
#GET http://localhost:4850/actions-for?coord=e2
# moves for: GET /moves-for?coord="insertcoordinate"
# import GUI and other important functionalities of the project


"""
# copy paste these variables for rules engine 
# these are all the possible post and get requests we can make

# Queries (using .get)
whoseTurn = requests.get(url = URL + "whose-turn")
isDone = requests.get(url = URL + "is-done")
##### not sure if i need this one ####
# newGame = requests.get(url = URL + "new-game")
gameState =  requests.get(url = URL + "game-state")
actionsFor = requests.get(url = URL + "actions-for")
pieceAt = requests.get(url = URL + "piece-at")
actionsSince = requests.get(url = URL + "actions-since")
currentAction = requests.get(url = URL + "curr-action-idx")

# Actions (using .post)
act = requests.post(url = URL + "act")
endTurn = requests.post(url = URL + "end-turn")
saveState = requests.post(url = URL + "save-state")
restoreState = requests.post(url = URL + "restore-state")

"""

# this is the start of the code

import requests
URL = "http://localhost:4850/"

isDone = False
isThreat = False
white = 'W'
black = 'B'
# pieces Dict shows initial pieces of board, change as coordinates are called
# _r indicates right side as seen from eyes of AI looking at board (f-h)
# _l indicates left side as seen from eyes of AI looking at board (a-c)
# pawn numbering begins on left side and increases (P8 is on h2 starting)
###############this is a placeholder dict until we get rules engine, need to know format and how to import currentboard variable ##########
defaultPieces = {
    "e1": "K",
    "d1": "Q",
    "f1": "P_r",
    "c1": "P_l",
    "g1": "N_r",
    "b1": "N_l",
    "h1": "A_r",
    "a1": "A_l",
    "a2": "I1",
    "b2": "I2",
    "c2": "I3",
    "d2": "I4",
    "e2": "I5",
    "f2": "I6",
    "g2": "I7",
    "h2": "I8",
    "e8": "k",
    "d8": "q",
    "c8": "p_r",
    "f8": "p_l",
    "b8": "n_r",
    "g8": "n_l",
    "a8": "a_r",
    "h8": "a_l",
    "h7": "i1",
    "g7": "i2",
    "f7": "i3",
    "e7": "i4",
    "d7": "i5",
    "c7": "i6",
    "b7": "i7",
    "a7": "i8"
}
# sets default piece positions based on if the AI has black or white
def ai_team(board):
    team = ''
    if board[0] == white:
        team = white
    else:
        team = black
    return team

       
def main():
    newGame = requests.get(url = URL + "new-game")
    gameState =  requests.get(url = URL + "game-state")
    team = ai_team(gameState.text)
    print("Team" + team) 


if __name__=="__main__":
    main()
   

# updates coordinates
def update_coord():
    ################use get coordinate function from rules################
    return "none" 

"""
###I dont think i need this but i like the ascii idea#######
# creates list of board coord from a1 ... h8
def create_coord(gameState):
    #ascii range for letters a - h
    coord = {}
    strt, end = 97,104
    count = 1
    for i in range(1, 9):
        for j in range(strt,end+1): 
            coord[(chr(j) + str(i))] = ''
    for x in range(1, len(gameState)):
        coord[x] = gameState[x]

    print(coord)
    return coord

#creates dictionary of coordinates and pieces
# takes team as req param, coord is optional to pass from def coordinates
def create_dict(team, defaultPiece, coord = []):
    pieces = ['K', 'Q', 'P', 'P', 'N', 'N', 'A', 'A', 'I', 'I', 'I', 'I', 'I',
            'I', 'I', 'I'] 
    aidict = defaultPiece
    if team == black:
        pieces = [x.lower() for x in pieces]
    
    for i in coord:
        if i == defaultPiece[i]:
            continue
        else:
            aidict[i] = 'B'
    print(aidict)



def new_game():
    aiPiecesPos = ai_team()
    #shows current players turn
    player = (1 if team.upper()  == whoseTurn.upper() else 0)
    for x in aiPiecesPos:
        actions + "x"
    
############# GET whoseTurn RULES ENGINE ########################

def new_turn():
    #shows current players turn
    player = (1 if team  == whoseTurn.upper() else 0)

#### starting alpha beta pruning ##########
while (player == 1 && isDone == False):
    

#############get current board state from rules engine ################3
# cb = requests.get(url = gameState)
currentBoard = []  

    

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
