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
