import numpy as np

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



def node(board, depth):
    tracker = np.array([0, 0])
    teams = {"W":"White", "B": "Black"}
    if endgame or depth == 1000: #check if its an endgame state
        if win:
            return [1, 1]
        elif loose:
            return [-1, 1]
        else:
            return [0,1]
    else:
        for i in range(10):
            #saves board state
            # sets board state as board
            random_move(teams[board[0]])
            #pops board
            tracker = np.add( node(board, depth+1), tracker)
        return tracker
