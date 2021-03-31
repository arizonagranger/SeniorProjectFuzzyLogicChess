#ai
import random
import requests
import numpy as np
import math

URL = "http://localhost:4850/"
teams = {"W":"White", "B": "Black"}


def is_end():
        end = requests.get(url = URL +"is-done")
        if end == True:
            print("game ended")
            return True
        else:
            return False
            
def simulate():
    path = []
    if is_end():
        print("game ended")
        return 1
    else:
        board = requests.get(url = URL + "get-state")
        #if depth == 0:
	#root node
	#root_node(board, path)
         #   pass		
        moves = random_move(teams[board[0]])
        for i in range(len(moves)):
            act = requests.post(url = URL + "act?action-str="+moves[i])
            save = requests.post(url = URL + "save-state")
        		
        #node(board, depth+1)
        end = requests.post(url = URL + "end-turn")
        simulate()
	                
def random_move(team):
    delegates = ["L", "R", "K"]
    moves = []
    while len(delegates) > 0:
        del_moves = []
        del_pieces = requests.get(url = URL + "pieces?team=" + team + "&corp=" + delegates.pop(random.randrange(len(delegates)))).text.split(",")
        for piece in del_pieces:            
            del_moves = requests.get(url = URL + "actions-for?coord="+piece).text.split("\n")
        random_move = del_moves[random.randrange(len(del_moves))]  
        for i in range(len(random_move)):
            if random_move[i] == ">":
                random_move[i] == "%3e"
        moves.append(random_move)
    return moves


def reward(visit, win):
    reward = win/visit
    return reward
	
def root_node(board, node_list):
    node_list.append([random_move(teams[board[0]]), node(board, 0)])
   
"""   
def compare(node_list):
     best = node_list.pop(0)
    for nodes in node_list:
        if nodes[1][0]/nodes[1][1] > best[1][0]/best[1][1]:
            best = nodes
    return best[0]


            
   
def node(board, depth):
    tracker = np.array([0, 0])
    if depth == 1000: #check if its an endgame state
        #reward = is_end()
        return reward
    else:
            #saves board state
            save = requests.post(url = URL +"save-state")
            # sets board state as board
            #moves = random_move(teams[board[0]])
  	    #make_moves(moves) 	
            #board = requests.get(url = URL + "get-state")
            #pops board
            board = requests.post(url = URL + "restore-state") 
            tracker = np.add( node(board, depth+1), tracker)
        return tracker
"""     
def new_game():
    newGame = requests.get(url = URL + "new-game")
    board = requests.get(url = URL + "game-state")
    print(board.text)
    return board.text

def turn():
    if not is_end():
    	turn = requests.get(url = URL + "whose-turn")
    	return turn
    else:
    	print("end of game, team method shouldn't be called")    
def oppteam(team):
    if team == "Black":
    	return "White"
    else:
    	return "Black"
                     
# start of functions to call AI
def play_game():
    iterations = 50
    #tree = mcts()
    board = new_game()
    playerteam = teams[board[0]]
    aiteam = oppteam(playerteam)
    while True:
        if is_end():
    	    print("game is over")
    	    return False
        board = requests.get(url = URL + "game-state")
        print("board before move: " + board.text)
        print(random_move(playerteam))
        yourturn = input("enter a move: ")        
        playermove = requests.post(url = URL + "act?action-str="+ yourturn)
        board = requests.get(url = URL + "game-state")
        print(board.text)
        print("made the move")
        push = requests.post(url = URL + "save-state")
        end = requests.post(url = URL + "end-turn")
        """
        move = random_move(aiteam)
        for i in range(len(move)):
        	requests.post(url=URL + "act?action-str="+move[i])
        end = requests.post(url = URL + "end-turn")
        """
        for i in range(10):
            print("in simulation")
            simulate()
        board = requests.get(url = URL + "game-state")
        print("after ai move: " + board.text)
        
        #if game is over, stop the loop
       # for i in range(iterations):
        #    tree.select(board)
        #board = tree.choose(board,team)
        
#moves = random_move("White")
play_game()
#root_node(game.text)
