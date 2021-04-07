import requests
import re

HOSTNAME = "192.168.84.128"
PORT = "4850"

url = "http://" + HOSTNAME + ":" + PORT

whose_turn_req = url + "/whose-turn"
is_done_req = url + "/is-done"
end_turn_req = url + "/end-turn"
save_state_req = url + "/save-state"
restore_state_req = url + "/restore-state"
new_game_req = url + "/new-game"
game_state_req = url + "/game-state"
actions_req = url + "/actions-for"
piece_at_req = url + "/piece-at"

server_response = True


class Button:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 100
        self.h = 100
        self.text = ""
        self.color = (0, 0, 0)
        self.selectColor = (0, 0, 0)
        self.action = action

    def __init__(self, x, y, w, h, text, color, selectColor, action):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.color = color
        self.selectColor = selectColor
        self.action = action


def coords_to_notation(coords):
    letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
    return letters[coords[0]] + str(coords[1] + 1)


def notation_to_coords(notation):
    return [int(ord(notation[0]) - 97), int(notation[1]) - 1]


#function that gets the board state from the RulesEngine and returns a 2D array
def parse_board_state():
    pieces = []
    state = expand_spaces(requests.get(game_state_req).text[1:])

    for i in range(8):
        pieces.append([])
        for j in range(8):
            index = 2 * (i * 8 + j)
            pieces[i].append(state[index:index+2])

    return pieces

#replaces the numbers in board state notation with spaces
def expand_spaces(state):
    s = ""
    num = ""
    is_number = False

    for ch in state:
        if ch.isnumeric():
            is_number = True
            num += ch
        else:
            if is_number:
                for i in range(int(num)):
                    s += "  "
            is_number = False
            s += ch
    return s

#gets the team/color of the piece at [c, r]
def get_piece_color(pieces, r, c):
    if pieces[r][c][0].islower():
        return "white"
    else:
        return "black"


#gets the delegation of the piece at [c, r]
def get_piece_delegation(pieces, r, c):
    if pieces[r][c][1] == "K":
        return "red"
    elif pieces[r][c][1] == "L":
        return "blue"
    elif pieces[r][c][1] == "R":
        return "green"

#returns the file name of a piece
def get_image(name):
    s = ""
    if name[0].islower():
        s += "B"
    else:
        s += "W"

    s += name[0].upper()
    return s


def get_piece(coords):
    return requests.get(piece_at_req + "?coord=" + coords_to_notation(coords)).text.split("\n")


#take an input of cordinates of a pieces such as [2,6] and returns a list of coordinates that the piece can move to
def move_reader(piece):
    moves = requests.get(actions_req + "?coord=" + coords_to_notation(piece)).text.split("\n")
    move_coordinates = []
    for move in moves:
        if ">" in move:
            move = re.split(pattern=r"[>x=]", string=move)
            move_coordinates.append(notation_to_coords(move[1]))
    return move_coordinates


#checks the status of the RulesEngine server
def check_server():
    global server_response

    while True:
        try:
            requests.get(url, timeout=5)
            server_response = True
        except (requests.ConnectionError, requests.Timeout):
            print("Unable to connect to " + url)
            server_response = False
            break