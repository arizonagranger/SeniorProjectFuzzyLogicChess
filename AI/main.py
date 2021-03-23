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
# pieceAt = requests.get(url = URL + "piece-at")

#moves for: GET /moves-for?coord="insertcoordinate"

isDone = False
isThreat = False
white = 'W'
black = 'B'
# pieces Dict shows initial pieces of board, change as coordinates are called
# _r indicates right side as seen from eyes of AI looking at board (f-h)
# _l indicates left side as seen from eyes of AI looking at board (a-c)
# pawn numbering begins on left side and increases (P8 is on h2 starting)
###############this is a placeholder dict until we get rules engine, need to know format and how to import currentboard variable ##########
wpiecesDict = {
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
bpiecesDict = {
    "k": "e8",
    "q": "d8",
    "p_r": "c8",
    "p_l": "f8",
    "n_r": "b8",
    "n_l": "g8",
    "a_r": "a8",
    "a_l": "h8",
    "i1": "h7",
    "i2": "g6",
    "i3": "f5",
    "i4": "e7",
    "i5": "d7",
    "i6": "c7",
    "i7": "b7",
    "i8": "a7"
}
 
def create_dict(team):
    pieces = ['K', 'Q', 'P', 'P', 'N', 'N', 'A', 'A', 'I', 'I', 'I', 'I', 'I',              'I', 'I', 'I']
    aidict = {}
    if team == black:
        pieces = [x.lower() for x in pieces]
    for i in pieces:
      
        

    

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


