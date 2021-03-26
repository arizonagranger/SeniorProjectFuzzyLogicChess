import random
import requests
URL = "http://localhost:4850/"

def random_move(team):
    delegates = ["L", "R", "K"]
    moves = []
    while len(delegates) > 0:
        del_moves = []
        del_pieces = requests.get(url = URL + "pieces?team=" + team + "&corp=" + delegates.pop(random.randrange(len(delegates)))).text.split(",")
        for piece in del_pieces:
            del_moves += requests.get(url = URL + "actions-for?coord=" + piece).text.split("\n")
        random_move = del_moves[random.randrange(len(del_moves))]
        actions = requests.get(url = URL + "actions-for?coord=" + random_move) ##this would be where the ai would send to the move to rules and does everything with the board state
        moves.append(random_move)
    return moves


moves = random_move("Black")

for i in moves:
    print(i)
