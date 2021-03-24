import random
def random_move(team):
    boardCord = ["a", "b", "c", "d", "e", "f", "g", "h"]
    delegates = ["L", "R", "K"]
    moves = []
    while len(delegates) > 0:
        del_moves = []
        del_pieces = request.post(url = URL + "pieces?team=" + team + "&corp=" + delegates.pop(random.randrange(len(delegates)))).text.split(",")
        for piece in del_pieces:
            del_moves.append(request.post(url = URL + "actions-for?coord=" + boardCord[piece[0]]+str(piece[1]+1)).text.split("\n"))
        random_move = del_moves[random.randrange(len(del_moves))]
        submitMove(request.post(url = URL + "actions-for?coord=" + move)) ##this would be where the ai would send to the move to rules and does everything with the board state
        moves.append(random_move)
    return moves
















# import chessGUI
# import re
# ##import requests
# URL = "http://localhost:4850/"

# boardCord = ["a","b","c","d","e","f","g","h"]
# black_del_1 = []
# black_del_2 = []
# black_del_3 = []
# white_del_1 = []
# white_del_2 = []
# white_del_3 = []

# def get_del():
#     for x in range(len(chessGUI.piece_del)):
#         for y in range(len(chessGUI.piece_del[x])):
#             if chessGUI.piece_color[x][y] == 1:
#                 if chessGUI.piece_del[x][y] == 1:
#                     white_del_1.append([x, y])
#                 elif chessGUI.piece_del[x][y] == 2:
#                     white_del_2.append([x, y])
#                 elif chessGUI.piece_del[x][y] == 3:
#                     white_del_3.append([x, y])
#             if chessGUI.piece_color[x][y] == 2:
#                 if chessGUI.piece_del[x][y] == 1:
#                     black_del_1.append([x, y])
#                 elif chessGUI.piece_del[x][y] == 2:
#                     black_del_2.append([x, y])
#                 elif chessGUI.piece_del[x][y] == 3:
#                     black_del_3.append([x, y])



# def move_lists(piece):
#     #sends the request to rules for the list of moves
#     moves = "GET http://localhost:4850/actions-for?coord="+boardCord[piece[0]]+str(piece[1]+1)
#     return moves.split("")##split at the string that seperates the moves

# def submitMove(move):
#     "POST http://localhost:4850/act?action-str=e2%3Ee3"

# def move_reader(del_pieces):
#     move = "GET actions-since?action-idx=-1"
#     move_list = re.split(pattern=r"[>x=]", string=move)
#     move_list = re.split(pattern=r"[>x=]", string=move)
#     for x in range(len(del_pieces)):
#         if del_pieces[x] == [boardCord.index(move_list[0][0]), int(move_list[0][1]) - 1]:
#             if (move_list[3] == 's'):
#                 del_pieces[x] = [boardCord.index(move_list[2][0]), int(move_list[2][1]) - 1]
#             else:
#                 del_pieces[x] = [boardCord.index(move_list[1][0]), int(move_list[1][1]) - 1]
#             break

# def random(team):
#     delegates = []
#     if team == "black":
#         delegates = [black_del_1, black_del_2, black_del_3]
#     else:
#         delegates = [white_del_1, white_del_2, white_del_3]
#     moves = []
#     while len(delegates) > 0:
#         del_moves = []
#         del_pieces = delegates.pop(random(len(delegates)))
#         for piece in del_pieces:
#             del_moves.append(move_lists(piece)) ##request list of moves for piece
#         random_move = del_moves[random(del_moves)]
#         submitMove(random_move) ##this would be where the ai would send to the move to rules and does everything with the board state
#         move_reader(del_pieces)
#         moves.append(random_move)
