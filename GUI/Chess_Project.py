from tkinter import *
import requests
import threading

hostname = "192.168.84.128"
port_number = "4850"

url = "http://" + hostname + ":" + port_number

whose_turn_req = url + "/whose-turn"
is_done_req = url + "/is-done"
end_turn_req = url + "/end-turn"
save_state_req = url + "/save-state"
restore_state_req = url + "/restore-state"
new_game_req = url + "/new-game"
game_state_req = url + "/game-state"
actions_req = url + "/actions-for"
piece_at_req = url + "/piece-at"

root = None
update = True
server_response = True
piece_selected = ""

pieces = []


def on_click(self):
     print("Hello")


def parse_board_state():
    global pieces

    pieces = []
    state = expand_spaces(requests.get(game_state_req).text[1:])

    for i in range(8):
        pieces.append([])
        for j in range(8):
            index = 2 * (i * 8 + j)
            pieces[i].append(state[index:index+2])
    return pieces


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


def get_piece_color(r, c):
    if pieces[r][c][0].islower():
        return "white"
    else:
        return "black"


def get_piece_delegation(r, c):
    if pieces[r][c][1] == "K":
        return "red"
    elif pieces[r][c][1] == "L":
        return "blue"
    elif pieces[r][c][1] == "R":
        return "green"


def set_pieces(board):
    for i in range(8):
        for j in range(8):
            if pieces[j][i] != "  ":
                border = Canvas(board, bd=-2, width=34, height=34, bg=get_piece_delegation(j, i))
                piece = Canvas(board, bd=-2, width=30, height=30, bg=get_piece_color(j, i))
                piece.grid(row=j, column=i)
                border.grid(row=j, column=i)


def update_board_state():
    global root

    root = Tk()

    title = Label(root, text="AI Chess Project (CS 4850)", font=("Calibri", 32, 'bold'))
    title.pack(padx=20, pady=20)

    settings = Button(root, text="...", bd=0, bg="#888")
    settings.place(width=40, height=40, rely=0, relx=1, x=-20, y=20, anchor=NE)

    main_content = Frame(root, width=400, height=400)

    # Left Panel
    left_panel = Frame(main_content, width=200, height=400)

    previous_moves = Frame(left_panel, width=200, height=100, bd=5, bg="#CCC", relief=RAISED)

    moves_title = Label(previous_moves, text="Previous Moves", font=("Calibri", 20, 'bold'), bd=-2, bg="#CCC")
    moves_title.pack(pady=10)
    moves_content = Frame(previous_moves, width=200, height=80, bd=-2, bg="#CCC")
    moves_content.pack(padx=20, pady=20)

    dice_rolls = Frame(left_panel, width=200, height=400, bd=5, bg="#CCC", relief=RAISED)

    dice_title = Label(dice_rolls, text="Dice Roll Table", font=("Calibri", 20, 'bold'), bd=-2, bg="#CCC")
    dice_title.pack(pady=10)
    dice_content = Frame(dice_rolls, width=220, height=200, bd=10, bg="#AAA", relief=SUNKEN)
    dice_content.pack(padx=10, pady=10)

    previous_moves.grid(row=0, column=0, pady=20)
    dice_rolls.grid(row=1, column=0)

    left_panel.grid(row=0, column=0, padx=20, pady=20)

    # Main Chess Board
    main_board = Frame(main_content, width=400, height=400)

    board = Frame(main_board, width=400, height=400, bd=20, bg="#444", relief=RAISED)

    for i in range(8):
        for j in range(8):
            tile = Canvas(board, bd=-2, width=50, height=50)
            # tile.bind("<Button-1>", on_click)
            if (i + j) % 2 == 0:
                tile.configure(bg="white")
            else:
                tile.configure(bg="black")
            tile.grid(row=j, column=i)

    set_pieces(board)

    board.pack(padx=100, pady=50, fill=Y)

    action_buttons = Frame(main_board, bd=20)

    move_button = Button(action_buttons, width=10, height=1, text="Move", font=("Calibri", 24, 'bold'), bg="#888", fg="#fff")
    attack_button = Button(action_buttons, width=10, height=1, text="Attack", font=("Calibri", 24, 'bold'), bg="#888", fg="#fff")
    delegate_button = Button(action_buttons, width=10, height=1, text="Delegate", font=("Calibri", 24, 'bold'), bg="#888", fg="#fff")

    move_button.grid(row=0, column=0, padx=10)
    attack_button.grid(row=0, column=1, padx=10)
    delegate_button.grid(row=0, column=2, padx=10)
    action_buttons.pack()

    main_board.grid(row=0, column=1)

    # Right Panel
    right_panel = Frame(main_content, width=200, height=400)

    captured_pieces = Frame(right_panel, width=200, height=600, bd=5, bg="#CCC", relief=RAISED)

    captured_title = Label(captured_pieces, text="Pieces Captured", font=("Calibri", 20, 'bold'), bd=-2, bg="#CCC")
    captured_title.pack(padx=20, pady=20)
    captured_content = Frame(captured_pieces, width=200, height=380, bd=-2, bg="#CCC")
    captured_content.pack(padx=20, pady=20)

    captured_pieces.grid(row=0, column=0)

    right_panel.grid(row=0, column=2, padx=20, pady=20)

    main_content.pack()

    return root


def check_server():
    global root, update, server_response

    while update:
        try:
            requests.get(url, timeout=5)
            server_response = True
        except (requests.ConnectionError, requests.Timeout):
            print("Unable to connect to " + url)
            server_response = False
            break


def main_loop():
    global root, update, pieces

    parse_board_state()
    print(pieces)
    root = update_board_state()
    while update:
        root.update()


def main():
    global update, server_response

    server_thread = threading.Thread(target=check_server)
    server_thread.start()

    if server_response:
        requests.get(new_game_req)

        main_thread = threading.Thread(target=main_loop)
        main_thread.start()

        while server_thread.is_alive() and main_thread.is_alive():
            continue

        update = False
        main_thread.join()
    server_thread.join()


if __name__ == '__main__':
    main()