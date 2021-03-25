import requests

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
        try:
            if int(ch):
                is_number = True
                num += ch
        except ValueError:
            if is_number:
                for i in range(int(num)):
                    s += "  "
            is_number = False
            s += ch
    return s


def get_image(name):
    s = ""
    if name[0].islower():
        s += "B"
    else:
        s += "W"

    s += name[0].upper()
    return s


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