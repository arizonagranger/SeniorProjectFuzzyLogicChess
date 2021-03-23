from tkinter import *

piece_color = \
    [[2, 2, 2, 2, 2, 2, 2, 2],
     [2, 2, 2, 2, 2, 2, 2, 2],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 1, 1, 1, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1]]
piece_type = \
    [[2, 3, 4, 5, 6, 4, 3, 2],
     [1, 1, 1, 1, 1, 1, 1, 1],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 1, 1, 1, 1, 1, 1],
     [2, 3, 4, 5, 6, 4, 3, 2]]
piece_del = \
    [[1, 1, 1, 3, 3, 2, 2, 2],
     [1, 1, 1, 3, 3, 2, 2, 2],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0],
     [2, 2, 2, 3, 3, 1, 1, 1],
     [2, 2, 2, 3, 3, 1, 1, 1]]


def on_click():
    print("Click")


def get_piece_color(r, c):
    if piece_color[r][c] == 1:
        return "white"
    elif piece_color[r][c] == 2:
        return "black"


def get_piece_delegation(r, c):
    if piece_del[r][c] == 1:
        return "red"
    elif piece_del[r][c] == 2:
        return "blue"
    elif piece_del[r][c] == 3:
        return "green"


def set_pieces(board):
    for i in range(8):
        for j in range(8):
            if piece_type[j][i] != 0:
                border = Canvas(board, bd=-2, width=34, height=34, bg=get_piece_delegation(j, i))
                piece = Canvas(board, bd=-2, width=30, height=30, bg=get_piece_color(j, i))
                piece.grid(row=j, column=i)
                border.grid(row=j, column=i)


def main():
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

    root.mainloop()


if __name__ == '__main__':
    main()