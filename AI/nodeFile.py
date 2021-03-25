import numpy as np
import requests
import random

URL = "http://localhost:4850/"
teams = {"W":"White", "B": "Black"}


#for the gui
#pass coordinate in notation: "a7, e3, etc"
def get_moves(piece):
    moves = requests.get(url = URL + "actions-for?coord=" + piece)
    return moves.text.split("\n")
def send_move(move):
    act = requests.post(url = URL + "act?action-str="+move.replace(">","%3e"))
    save = requests.post(url = URL + "save-state")
def current_state():
    board = requests.get(url = URL + "game-state")
    return board
def previous_action():
    current = requests.get(url = URL + "curr-action-idx")
    return requests.get(url = URL + "actions-since?action-idx="+current)
#endgame and win functions can be used for gui too


def root_node(board):
    node_list = []
    for i in range(10):
        #save
        node_list.append([random_move(teams[board[0]]), node(board, 0)])

    best = node_list.pop(0)
    for nodes in node_list:
        if nodes[1][0]/nodes[1][1] > best[1][0]/best[1][1]:
            best = nodes
    return best[0]

def endgame():
    end = requests.get(url = URL +"is-done")
    if end == True:
        print("game ended")
        return True
    else:
        return False
            
def random_move(team):
    delegates = ["L", "R", "K"]
    moves = []
    while len(delegates) > 0:
        del_moves = []
        del_pieces = requests.get(url = URL + "pieces?team=" + team + "&corp=" + delegates.pop(random.randrange(len(delegates)))).text.split(",")
        for piece in del_pieces:            
            del_moves = requests.get(url = URL + "actions-for?coord="+piece).text.split("\n")
        random_move = del_moves[random.randrange(len(del_moves))]  
        act = requests.post(url = URL + "act?action-str=" + random_move.replace(">","%3e"))
        save = requests.post(url = URL + "save-state")

        moves.append(random_move)
    return moves
    
def win():
    board = requests.get(url = URL + "get-state")
    if teams[board[0]] == "Black":
        return True
    else:
        return False

def node(board, depth):
    #end turn here
    tracker = np.array([0, 0])
    teams = {"B":"White", "W": "Black"}
    if endgame or depth == 1000: #check if its an endgame state
        if win:
            return [1, 1]
        else:
            return [0,1]
    else:
        for i in range(10):
            # saves board state
            # sets board state as board
            random_move(teams[board[0]])
            #pops board
            tracker = np.add( node(board, depth+1), tracker)
        return tracker

def play_game():
    new = requests.get(url = URL + "new-game")
    board = requests.get(url = URL + "game-state")
    while not endgame():
      #  for i in range(3):
       #     move = input("put a move down: ")
            
        wmoves = random_move(teams[board.text[0]])
        end = requests.post(url = URL + "end-turn")
        board = requests.get(url = URL + "game-state")
        print(wmoves)
        for i in range(3):
            while True:
                y = input("Type 'y' if you want to see moves for a specific coordinate: ")        
                if y == "y":
                    coord = input("Type in a coordinate: ")
                    actions = requests.get(url = URL + "actions-for?coord=" + coord)
                    print(actions.text)
                else: 
                    break
            move = input("make a move: ")
            act = requests.post(url = URL + "act?action-str="+move)
        end = requests.post(url = URL + "end-turn")
        board = requests.get(url = URL + "game-state")


play_game()
