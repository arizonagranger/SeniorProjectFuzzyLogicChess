# written by Haley Granger
# Senior Project AI Chess
"""
####anytime you see multiple of these it means we need stuff from the rules engine#######################
# import AI Rules Engine
# How do i do this? IDK
##%3E
#Example requests:
#POST http://localhost:4850/act?action-str=e2%3Ee3
#GET http://localhost:4850/new-game
#POST http://localhost:4850/end-turn
#GET http://localhost:4850/actions-for?coord=e2

# import GUI and other important functionalities of the project


############ requests, do this once rakudo is working #############
# import requests
# URL = "http://localhost:4850/"
# whoseTurn = requests.get(url = URL + "whose-turn")
# isDone = requests.get(url = URL + "is-done")
# endTurn = requests.get(url = URL + "end-turn")
# saveState = requests.get(url = URL + "save-state")
# restoreState = requests.get(url = URL + "restore-state")
# newgame = requests.get(url = URL + "new-game")
# gameState =  requests.get(url = URL + "game-state")
# actions = requests.get(url = URL + "actions-for")

#moves for: GET /moves-for?coord="insertcoordinate"
"""
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
        
def main():
   create_coord()
   # create_dict(white, defaultPieces, c)


#creates dictionary of coordinates and pieces
#possible other parameters
# def create_dict(team, coord, defaultPiece):
def create_dict(coord, defaultPiece = {}):
    pieces = ['K', 'Q', 'P', 'P', 'N', 'N', 'A', 'A', 'I', 'I', 'I', 'I', 'I',
            'I', 'I', 'I'] 
    aiDict = defaultPiece
 # i think this is unnecessary
 #   if team == black:
 #       pieces = [x.lower() for x in pieces]
    for i in coord:
        aiDict[i] = gameState[i+1]
        print(gameState[i+1]
    print(aiDict)
 
# updates coordinates
def update_coord(piece):
    ################use get coordinate function from rules################
    return "none" 

# creates list of board coord from a1 ... h8
def create_coord():
    #ascii range for letters a - h
    coord = []
    strt, end = 97,104
    for i in range(1, 9):
        for j in range(strt,end+1):
            coord.append(chr(j) + str(i))
    return coord


if __name__=="__main__":
    main()
    
"""
def new_game():
    aiPiecesPos = ai_team()
    #shows current players turn
    player = (1 if team.upper()  == whoseTurn.upper() else 0)
    for x in aiPiecesPos:
        actions + "x"
    

# sets default piece positions based on if the AI has black or white
team = ''
def ai_team():
    if currentBoard[0] = white:
        team = white
        aipiecesDict = create_dict(white) 
    else:
        team = black
        aipiecesDict = create_dict(black)
    return aipiecesDict

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
