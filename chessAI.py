import numpy as np

currentBoard = []
boardCord = ["a","b","c","d","e","f","g","h"]

#lets me mimmic the rules egine
def board_server():
    return input("server response: ")

#gives me the pieces and number of spaces
def seperate_string_number(string):
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
#this can also be used for the ai to find pieces that can attack a certain piece
def check_threats(piece):
    threats = []
    for x in range(8):
        for y in range(8):
            if currentBoard[x][y].isupper() != currentBoard[piece[0]][piece[1]].isupper() and currentBoard[x][y] != " ":
                if "x"+boardCord[piece[0]]+str(piece[1]+1) in board_server():
                    threats.append([x, y])
    return threats



currentBoard = boarState("ANPQKPNAIIIIIIII32iiiiiiiianpqkpna")
check_threats([5,2])
