import numpy as np
import chessGUI

currentBoard = []
boardCord = ["a","b","c","d","e","f","g","h"]

def get_del(delegation, team):
    del_list = []
    for x in range(len(chessGUI.piece_del)):
        for y in range(len(chessGUI.piece_del[x])):
            if chessGUI.piece_del[x][y] == delegation and chessGUI.piece_color[x][y] == team:
                del_list.append([x, y])
    return del_list

def move_lists(piece):
    #sends the request to rules for the list of moves
    moves = "this is the string the engine would return"
    return moves.split("")##split at the string that seperates the moves


def submitMove(move):
    ##"sends move to the rules engine"
    return 0

def random():
    delegates = ["LB", "KQ", "RB"]
    moves = []
    while len(delegates) > 0:
        delMoves = []
        delPieces = delegates.pop(random(len(delegates)))## this is where the ai request the list of pieces in the delegation
        for piece in delPieces:
            delMoves.append(move_lists(piece)) ##request list of moves for pieve
        randomMove = delMoves[random(delMoves)]
        submitMove(randomMove) ##this would be where the ai would send to the move to rules and does everything with the board state
        moves.append(randomMove)



















#lets me mimmic the rules egine
def board_server():
    return input("server response: ")

#gives me the pieces and number of spaces
def seperate_string_number(string):
    string = string.replace(string[0],'',1)
    previous_character = string[0]
    groups = []
    newword = string[0]
    for x, i in enumerate(string[1:]):
        if i.isalpha() and previous_character.isalpha():
            newword += i
        elif i.isnumeric() and previous_character.isnumeric():
            newword += i
        else:
            groups.append(newword)
            newword = i

        previous_character = i

        if x == len(string) - 2:
            groups.append(newword)
            newword = ''
    return groups

#creates a 2d array form the board string given by rules engine
def boarState(state):
    board = []
    for x in seperate_string_number(state):
        if(x.isnumeric()):
            for y in range(int(x)):
                board.append(" ")
        else:
            for y in x:
                board.append(y)
    return(np.reshape(np.array(board), (8, 8)))

#scans throught the board and checks for any threats on the given piece
def check_threats(piece):
    threats = []
    for x in range(8):
        for y in range(8):
            if currentBoard[x][y].isupper() == currentBoard[piece[0]][piece[1]].isupper() and currentBoard[x][y] != " ":
                if "x"+boardCord[piece[0]]+str(piece[1]+1) in board_server():
                    threats.append([x, y])
    return threats









# currentBoard = boarState("WANPQKPNAIIIIIIII32iiiiiiiianpqkpna")
# check_threats([5,2])
print(get_del(1,1))
