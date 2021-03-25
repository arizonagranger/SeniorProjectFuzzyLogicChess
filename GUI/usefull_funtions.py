import re

##this takes the string that the rules engine gives and alters the GUI's 2d array to match the board state
def board_state(board):
    types = {
        'i': 1, 'a': 2, 'n': 3, 'p': 4, 'q': 5, 'k': 6
    }

    delegations = {
        'L': 2, 'K': 3, 'R': 1
    }

    board = board[1:]
    x = 0
    while len(board) > 0:
        if not board[0].isnumeric():
            piece = board[:2]
            board = board[2:]
            if piece[0].isupper():
                piece_color[int(x/8)][x % 8] = 2
            else:
                piece_color[int(x / 8)][x % 8] = 1
            piece_type[int(x/8)][x % 8] = types[piece[0].lower()]
            piece_del[int(x/8)][x % 8] = delegations[piece[1]]
            x += 1
        else:
            if len(board) > 1 and board[1].isnumeric():
                number = board[:2]
                board = board[2:]
            else:
                number = board[:1]
                board = board[1:]
            for y in range(int(number)):
                piece_del[int(x / 8)][x % 8] = 0
                piece_type[int(x / 8)][x % 8] = 0
                piece_color[int(x / 8)][x % 8] = 0
                x += 1

                
#takes the cordinates for a piece in an array for example [2,7] and returns a list of all the cordinates that that piece can move to                
def move_reader(piece):
    boardCord = ["a", "b", "c", "d", "e", "f", "g", "h"]
    moves = requests.get(url = URL + "actions-for?coord=" + boardCord.piece[0] + str(piece[1]+1)).text.split("\n")
    move_cordinates = []
    for move in moves:
        move = re.split(pattern=r"[>x=]", string=move)
        move_cordinates.append([boardCord.index(move[1][0]), int(move[1][1])])
    return move_cordinates
