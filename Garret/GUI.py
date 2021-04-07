## controls: left mouse move, right mouse attack, middle mouse delegate, any key ends turn

import pygame as p
import Board as b
import RandomAI as ai
import random

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
OFFSET = [(SCREEN_WIDTH - WIDTH) / 2, (SCREEN_HEIGHT - HEIGHT) / 2 - 20]

INITIAL_STATE = "WAKNRPRQKKKPLNLAKIRIRIRIKIKILILIL32iLiLiLiKiKiRiRiRaKnLpLqKkKpRnRaK"
BOARD = b.Board(INITIAL_STATE)
SCREEN = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
AI = ai.RandomAI(BOARD, 1)
PIECE = None
DICE_ROLL = 0
TOOLTIP = []

MOUSE_POS = []
IMAGES = {}
SQUARES = []
BUTTONS = []
PIECE_COORDS = []

TEAM = {0: "White", 1: "Black"}
UNIT = {"a": "Rook", "i": "Pawn", "k": "King", "n": "Knight", "p": "Bishop", "q": "Queen"}
DELEGATION = {"K": "King", "L": "Left Bishop", "R": "Right Bishop"}
MOVES = [["King: "], ["Left Bishop: "], ["Right Bishop: "]]

GAME_RUNNING = True


def main():
    start_game()

    while GAME_RUNNING:
        update_game()
    quit_game()


def start_game():
    p.init()
    p.display.set_caption("Medieval Fuzzy Logic Chess")
    load_images()
    set_buttons()
    new_game()


def new_game():
    global BOARD, AI, PIECE, DICE_ROLL, PIECE_COORDS, GAME_RUNNING

    BOARD = b.Board(INITIAL_STATE)
    AI = ai.RandomAI(BOARD, 1)
    PIECE = None
    DICE_ROLL = random.randint(1, 6)
    PIECE_COORDS = []
    GAME_RUNNING = True

    clear_moves()


def update_game():
    global GAME_RUNNING

    draw_game()
    for event in p.event.get():
        if event.type == p.QUIT:
            GAME_RUNNING = False
        mouse_event(event)

    if BOARD.turn == 1:
        AI.ai_move()


def end_turn():
    global PIECE, PIECE_COORDS

    PIECE = None
    PIECE_COORDS = []

    BOARD.end_turn()
    clear_moves()


def quit_game():
    p.quit()
    quit()


def load_images():
    units = ["a", "i", "p", "q", "k", "n"]
    corps = ["L", "K", "R"]

    for unit in units:
        for corp in corps:
            for team in range(2):
                img = p.image.load("images/" + str(team) + unit + corp + ".png")
                IMAGES[str(team) + unit + corp] = p.transform.scale(img, (60, 60))

    for dice in range(1, 7):
        img = p.image.load("images/Dice" + str(dice) + ".png")
        IMAGES["dice" + str(dice)] = p.transform.scale(img, (148, 148))


def set_buttons():
    Button(62, 198, 260, 68, "New Game", p.Color("gray"), new_game)
    Button(62, 298, 260, 68, "Reset Turn", p.Color("gray"), None)
    Button(510, 624, 260, 68, "End Turn", p.Color("gray"), end_turn)


def draw_game():
    SCREEN.fill(p.Color("white"))
    draw_squares()
    draw_moves()
    draw_pieces()
    draw_buttons()
    draw_text()
    draw_dice()
    draw_tooltip()
    p.display.flip()


def draw_squares():
    colors = [p.Color("white"), p.Color("gray")]
    p.draw.rect(SCREEN, p.Color("black"), p.Rect(OFFSET[0] - 5, OFFSET[1] - 5, WIDTH + 10, HEIGHT + 10))

    for x in range(DIMENSION):
        for y in range(DIMENSION):
            color = colors[(x + y) % 2]
            s = p.draw.rect(SCREEN, color, p.Rect(x * SQ_SIZE + OFFSET[0], y * SQ_SIZE + OFFSET[1], SQ_SIZE, SQ_SIZE))
            if len(SQUARES) <= pow(DIMENSION, 2):
                SQUARES.append((s, x, y))


def draw_moves():
    if PIECE is not None:
        colors = [p.Color("cyan"), p.Color("red")]

        for x in range(DIMENSION):
            for y in range(DIMENSION):
                if [y, x] in BOARD.get_moves(PIECE_COORDS):
                    p.draw.rect(SCREEN, colors[0], p.Rect(x * SQ_SIZE + OFFSET[0], y * SQ_SIZE + OFFSET[1], SQ_SIZE, SQ_SIZE))
                elif [y, x] in BOARD.get_attacks(PIECE_COORDS):
                    p.draw.rect(SCREEN, colors[1], p.Rect(x * SQ_SIZE + OFFSET[0], y * SQ_SIZE + OFFSET[1], SQ_SIZE, SQ_SIZE))


def draw_pieces():
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            piece = BOARD.board[y][x]
            if piece is not None:
                img_name = str(piece.team) + piece.unit + piece.delegation
                SCREEN.blit(IMAGES[img_name], p.Rect(x * SQ_SIZE + OFFSET[0], y * SQ_SIZE + OFFSET[1], SQ_SIZE, SQ_SIZE))


def draw_buttons():
    for b in BUTTONS:
        b.draw_button()


def draw_text():
    spacing = 0
    text_objects = [("Medieval Fuzzy Logic Chess", 640, 40, 40), ("Dice Roll:", 192, 442, 32),
                    ("Moves:", 1088, 128, 32), ("Pieces Captured:", 1088, 320, 32)]

    for text in text_objects:
        text_font = p.font.SysFont("Calibri", text[3], True)
        text_font.set_underline(True)
        text_obj = text_font.render(text[0], True, p.Color("black"))
        text_size = text_obj.get_size()
        SCREEN.blit(text_obj, (text[1] - text_size[0] / 2, text[2] - text_size[1] / 2))

    for move in MOVES:
        for text in move:
            text_font = p.font.SysFont("Calibri", 20)
            text_obj = text_font.render(text, True, p.Color("black"))
            text_size = text_obj.get_size()
            SCREEN.blit(text_obj, (1088 - text_size[0] / 2, 170 - text_size[1] / 2 + spacing))
            spacing += text_size[1] + 5
        spacing += 5


def draw_dice():
    SCREEN.blit(IMAGES["dice" + str(DICE_ROLL)], p.Rect(118, 472, 148, 148))


def draw_tooltip():
    if len(TOOLTIP) != 0:
        spacing = 0
        dimensions = [0, 4]
        text_font = p.font.SysFont("Calibri", 20, False, True)

        for text in TOOLTIP:
            text_obj = text_font.render(text, True, p.Color("black"))
            text_size = text_obj.get_size()
            if dimensions[0] < text_size[0]:
                dimensions[0] = text_size[0] + 8
            dimensions[1] += text_size[1] + 5

        p.draw.rect(SCREEN, p.Color(240, 240, 240), p.Rect(MOUSE_POS[0] + 8, MOUSE_POS[1] + 8, dimensions[0] + 4, dimensions[1] + 4))
        p.draw.rect(SCREEN, p.Color("white"), p.Rect(MOUSE_POS[0] + 10, MOUSE_POS[1] + 10, dimensions[0], dimensions[1]))

        for text in TOOLTIP:
            text_obj = text_font.render(text, True, p.Color("black"))
            SCREEN.blit(text_obj, (MOUSE_POS[0] + 14, MOUSE_POS[1] + spacing + 14))
            spacing += text_obj.get_size()[1] + 5


def update_moves(action=-1, start_pos=[], end_pos=[]):
    clear_moves(False)

    del_index = {"K": 0, "L": 1, "R": 2}
    del_name = {"K": "King", "L": "Left Bishop", "R": "Right Bishop"}

    if PIECE is not None:
        delegation = PIECE.delegation
        if action == 0:
            MOVES[del_index[delegation]][0] = del_name[delegation] + ": Moved " + str(start_pos) + " to " + str(end_pos)
        elif action == 1:
            if PIECE.unit == "n":
                MOVES[del_index[delegation]].append("and successfully attacked " + str(end_pos) + " (" + str(DICE_ROLL) + ")")
            else:
                MOVES[del_index[delegation]][0] = del_name[delegation] + ": " + str(start_pos) + " successfully attacked " + str(end_pos) + " (" + str(DICE_ROLL) + ")"
        elif action == 2:
            if PIECE.unit == "n":
                MOVES[del_index[delegation]].append("and failed to attack " + str(end_pos) + " (" + str(DICE_ROLL) + ")")
            else:
                MOVES[del_index[delegation]][0] = del_name[delegation] + ": " + str(start_pos) + " failed to attack " + str(end_pos) + " (" + str(DICE_ROLL) + ")"
        elif action == 3:
            MOVES[del_index[delegation]][0] = del_name[delegation] + ": Delegate"


def clear_moves(reset=True):
    global MOVES

    if reset:
        MOVES = [["King: "], ["Left Bishop: "], ["Right Bishop: "]]
        update_moves()


def mouse_event(event):
    global PIECE, PIECE_COORDS, MOUSE_POS, TOOLTIP

    TOOLTIP = []
    MOUSE_POS = p.mouse.get_pos()
    selected_square = [s for s in SQUARES if s[0].collidepoint(MOUSE_POS)]
    selected_button = [b for b in BUTTONS if b.rect.collidepoint(MOUSE_POS)]

    if len(selected_square) != 0:
        col = selected_square[0][2]
        row = selected_square[0][1]

    if event.type == p.MOUSEBUTTONDOWN:
        if len(selected_square) != 0:
            if len(PIECE_COORDS) == 0:
                if BOARD.board[col][row] is not None and BOARD.get_piece([col, row]).team == 0:
                    PIECE_COORDS = [col, row]
                    PIECE = BOARD.get_piece(PIECE_COORDS)
            else:
                if event.button == 1:
                    if BOARD.board[col][row] is not None and BOARD.get_piece([col, row]).team == 0:
                        PIECE_COORDS = [col, row]
                        PIECE = BOARD.get_piece(PIECE_COORDS)
                        return
                    else:
                        move_piece(col, row)
                elif event.button == 3:
                    attack_piece(col, row)
                elif event.button == 2:
                    delegate_piece(col, row)
                PIECE_COORDS = []
                PIECE = None
        elif len(selected_button) != 0:
            selected_button[0].action()

    if len(selected_square) != 0:
        if PIECE is not None:
            TOOLTIP.append(get_notation([row, col]))
            if [col, row] in BOARD.get_moves(PIECE_COORDS):
                TOOLTIP.append("Left-click to move")
            elif [col, row] in BOARD.get_attacks(PIECE_COORDS):
                TOOLTIP.append("Right-click to attack")
                TOOLTIP.append("Chance of success: " + str(get_success_rate(PIECE_COORDS, [col, row])) + " / 6")
            elif [col, row] == PIECE_COORDS:
                TOOLTIP.append("Middle-click to change delegation")
            elif BOARD.get_piece([col, row]) is not None:
                piece_info = piece_to_string(BOARD.get_piece([col, row]))
                TOOLTIP = [get_notation([row, col]) + ": " + piece_info[0], piece_info[1], "Click to cancel"]
            else:
                TOOLTIP.append("Click to cancel")
        elif BOARD.get_piece([col, row]) is not None:
            piece_info = piece_to_string(BOARD.get_piece([col, row]))
            if BOARD.get_piece([col, row]).team == 0:
                TOOLTIP = [get_notation([row, col]) + ": " + piece_info[0], piece_info[1], "Left-click for options"]
            else:
                TOOLTIP = [get_notation([row, col]) + ": " + piece_info[0], piece_info[1]]
        else:
            TOOLTIP.append(get_notation([row, col]))


def move_piece(col, row):
    if BOARD.move(PIECE_COORDS, [col, row]):
        update_moves(0, PIECE_COORDS, [col, row])


def attack_piece(col, row):
    global DICE_ROLL

    roll = BOARD.attack(PIECE_COORDS, [col, row])

    if roll[1] != 0:
        DICE_ROLL = roll[1]
        if roll[0] == 1:
            update_moves(1, PIECE_COORDS, [col, row])
        else:
            update_moves(2, PIECE_COORDS, [col, row])


def delegate_piece(col, row):
    update_moves(2, PIECE_COORDS, [col, row])
    BOARD.del_piece(PIECE_COORDS, BOARD.board[col][row].delegation)


def get_notation(coords):
    letters = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
    return letters[coords[0]] + str(8 - coords[1])


def piece_to_string(piece):
    return TEAM[piece.team] + " " + UNIT[piece.unit], "Delegation: " + DELEGATION[piece.delegation]


def get_success_rate(attacker, defender):
    return 7 - BOARD.attack_values[BOARD.get_piece(attacker).unit + BOARD.get_piece(defender).unit]


class Button:
    def __init__(self, x, y, w, h, text, color, action):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.color = color
        self.action = action
        BUTTONS.append(self)

    def draw_button(self):
        p.draw.rect(SCREEN, p.Color("black"), [self.x - 2, self.y - 2, self.w + 4, self.h + 4])
        self.rect = p.draw.rect(SCREEN, self.color, [self.x, self.y, self.w, self.h])
        text_font = p.font.SysFont("Calibri", 32)
        text_obj = text_font.render(self.text, True, p.Color("black"))
        text_size = text_obj.get_size()
        SCREEN.blit(text_obj, (self.x + self.w / 2 - text_size[0] / 2, self.y + self.h / 2 - text_size[1] / 2))


if __name__ == '__main__':
    main()
