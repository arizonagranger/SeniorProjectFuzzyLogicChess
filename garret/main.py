# import random
# import requests
#
# URL = "http://localhost:4850/"
#

def random_move(team):
    boardCord = ["a", "b", "c", "d", "e", "f", "g", "h"]
    delegates = ["L", "R", "K"]
    moves = []
    while len(delegates) > 0:
        del_moves = []
        del_pieces = requests.post(
            url=URL + "pieces?team=" + team + "&corp=" + delegates.pop(random.randrange(len(delegates)))).text.split(
            ",")
        for piece in del_pieces:
            del_moves.append(
                requests.post(url=URL + "actions-for?coord=" + boardCord[piece[0]] + str(piece[1] + 1)).text.split(
                    "\n"))
        random_move = del_moves[random.randrange(len(del_moves))]
        submitMove(requests.post(
            url=URL + "actions-for?coord=" + random_move))  ##this would be where the ai would send to the move to rules and does everything with the board state
        moves.append(random_move)
    return moves


print(random_move("Black"))