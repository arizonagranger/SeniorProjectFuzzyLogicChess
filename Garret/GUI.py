import pygame as p
import Board as Board
import RandomAI as RandAI
import AI as ai
import random
import time
import threading

# The resolution of the main window (16:9)
SCREEN_SIZE = [1280, 720]
# Width and height of the chess board
WIDTH = HEIGHT = 512
# The dimensions of the chess board (8x8)
DIMENSION = 8
# The size (in pixels) of each square on the chess board
SQ_SIZE = HEIGHT // DIMENSION
# The position of the top-left corner of the chess board
# Used to center the chess board within the window
OFFSET = [(SCREEN_SIZE[0] - WIDTH) / 2, (SCREEN_SIZE[1] - HEIGHT) / 2]

# Starting state of the board
#WAKNRPRQKKKPLNLAKIRIRIRIKIKILILIL32iLiLiLiKiKiRiRiRaKnLpLqKkKpRnRaK
INITIAL_STATE = "WAKNRPRQKKKPLNLAKIRIRIRIKIKILILIL32iLiLiLiKiKiRiRiRaKnLpLqKkKpRnRaK"
# Board object reference
BOARD = Board.Board(INITIAL_STATE)
# Create the main window display using the screen size
SCREEN = p.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
# AI object reference
RAI = RandAI.RandomAI(BOARD, 1)
AI2 = ai.AI(BOARD, 1)
AI = ai.AI(BOARD, 0)
# The currently selected chess piece; none if no piece is selected
PIECE = None
# The value of the last dice roll; 0 on start
DICE_ROLL = 0
# The list of strings that will appear in the tooltip object; empty on start
# Made as a list of strings since pygame doesn't support multi-line text
TOOLTIP = []
# The menu that is currently being displayed
CURRENT_MENU = "Main"

# The position of the mouse in the window (increasing from top-left to bottom-right corner)
MOUSE_POS = [0, 0]
# Dictionary of images
IMAGES = {}
# List of squares on the chess board so that they can be referenced
SQUARES = []
# List of buttons so that they can be referenced
BUTTONS = []
# List of captured pieces
CAPTURED_PIECES = []
# Coordinates of the currently selected piece (on the chess board)
PIECE_COORDS = []
# List of all positions the currently selected piece can move to
MOVE_LIST = []
# List of all positions the currently selected piece can attack
ATTACK_LIST = []
# The list of moves made in the current turn
# Made as a list of strings to support knight moves that overflow to next line
MOVES = [["King:"], ["Left:"], ["Right:"]]

# Dictionaries for replacing piece attributes with readable text
TEAM = {0: "White", 1: "Black"}
UNIT = {"a": "Rook", "i": "Pawn", "k": "King", "n": "Knight", "p": "Bishop", "q": "Queen"}
DELEGATION = {"K": "King", "L": "Left Bishop", "R": "Right Bishop"}

# Boolean that checks whether the game state is currently running
GAME_RUNNING = True

AI_THREAD = None
DICE_THREAD = None
PROCESSING = False
IS_ROLLING = False


def main():
    start_game()

    while GAME_RUNNING:
        update_game()
    quit_game()


# Actions that occur when the program first starts (should only be called once)
def start_game():
    # Pygame initialization
    p.init()
    # Sets the name of the window in the top-left corner of the display
    p.display.set_caption("Medieval Fuzzy Logic Chess")
    # Load the images and add them to the dictionary
    load_images()
    # Create the buttons and assign their actions
    set_buttons()
    # Set the UI to new game state
    new_game()


# Actions that occur whenever a new game is started
def new_game():
    global BOARD, AI, RAI, AI2, DICE_ROLL, CAPTURED_PIECES, CURRENT_MENU, GAME_RUNNING

    # Reset the board state
    BOARD = Board.Board(INITIAL_STATE)
    # BOARD.add_piece(0, "k", "K", [7, 0])
    # BOARD.add_piece(0, "k", "K", [6, 0])
    # BOARD.add_piece(1, "a", "R", [0, 0])
    # BOARD.add_piece(1, "a", "L", [0, 3])
    # BOARD.add_piece(1, "k", "K", [0, 7])
    # Reset the AI
    AI = RandAI.RandomAI(BOARD, 1)
    AI = ai.AI(BOARD, 0)
    AI2 = ai.AI(BOARD, 1)
    RAI = RandAI.RandomAI(BOARD, 1)
    # Sets the dice to a random number
    DICE_ROLL = random.randint(1, 6)
    # Clear captured pieces list
    CAPTURED_PIECES = []
    # Reset game menu to main menu
    CURRENT_MENU = "Main"
    # Set game running to true
    GAME_RUNNING = True

    # Reset other stats
    reset_state()


# Actions that occur every frame
def update_game():
    global GAME_RUNNING, AI_THREAD, PROCESSING

    # Draw UI graphics onto display
    draw_game()

    # Check if any events occur during frame
    for event in p.event.get():
        # Check if the game has ended
        if BOARD.state != 2 and CURRENT_MENU != "EndGame":
            change_menu("EndGame")
        # p.QUIT is called when the application closes
        if event.type == p.QUIT:
            GAME_RUNNING = False
        # Check for mouse events (clicks, hovering, etc.)
        mouse_event(event)

    # Do AI actions if not the player's turn
    if BOARD.turn == 1 and not PROCESSING:
        # AI.test_future_move()
        # BOARD.end_turn()
        # RAI.ai_move()

        PROCESSING = True
        AI_THREAD = threading.Thread(target=ai_thread, args=[1])
        AI_THREAD.start()


# Actions that occur when the player ends their turn
def end_turn(ai_playing=False):
    global AI_THREAD, PROCESSING

    if ai_playing:
        PROCESSING = True
        AI_THREAD = threading.Thread(target=ai_thread, args=[0])
        AI_THREAD.start()
    else:
        # Reset piece and moves list
        reset_state()
        # Tell Board object's that the player's turn has ended
        BOARD.end_turn()


def reset_state():
    global PIECE, PIECE_COORDS, MOVE_LIST, ATTACK_LIST, MOVES

    # Remove piece reference if one exists
    PIECE = None
    # Clear coordinates of piece
    PIECE_COORDS = []
    # Clear move list
    MOVE_LIST = []
    # Clear attack list
    ATTACK_LIST = []
    # Clear actions made if turn wasn't completed
    MOVES = [["King:"], ["Left:"], ["Right:"]]


# Actions that occur when the program is quitting
def quit_game():
    # End pygame session
    p.quit()
    # End Python program
    quit()


def ai_thread(turn):
    global AI_THREAD, PROCESSING, MOVES, PIECE

    MOVES = [["King:"], ["Left:"], ["Right:"], [""]]
    if turn == 0:
        AI.test_future_move()
        reset_state()
    else:
        for x in AI2.test_future_move():
            if len(x) == 4:
                if x[3][0] == 0:
                    PIECE = BOARD.get_piece(x[1])
                    update_moves(0, x[0], x[1], x[3][1])
                    update_moves(2, x[1], x[2], x[3][1])
                else:
                    PIECE = BOARD.get_piece(x[2])
                    update_moves(0, x[0], x[1], x[3][1])
                    update_moves(1, x[1], x[2], x[3][1])
            elif len(x) == 3:
                if x[2][0] == 0:
                    PIECE = BOARD.get_piece(x[0])
                    update_moves(2, x[0], x[1], x[2][1])
                elif BOARD.get_piece(x[0]) is None:
                    PIECE = BOARD.get_piece(x[1])
                    update_moves(1, x[0], x[1], x[2][1])
                else:
                    PIECE = BOARD.get_piece(x[0])
                    update_moves(1, x[0], x[1], x[2][1])
            else:
                PIECE = BOARD.get_piece(x[1])
                update_moves(0, x[0], x[1])
    BOARD.end_turn()
    AI_THREAD = False
    PROCESSING = False


# Loads images from file location into dictionary (for performance reasons)
def load_images():
    # Piece images are formatted as: (team + unit + corp).png
    # Dice images are formatted as: Dice(number).png
    units = ["a", "i", "p", "q", "k", "n"]

    # Load icons for buttons and add to dictionary
    IMAGES["newgame"] = p.transform.scale(p.image.load("images/NewGame.png").convert_alpha(), (32, 32))
    IMAGES["settings"] = p.transform.scale(p.image.load("images/Settings.png").convert_alpha(), (32, 32))
    IMAGES["endturn"] = p.transform.scale(p.image.load("images/EndTurn.png").convert_alpha(), (64, 64))
    IMAGES["close"] = p.transform.scale(p.image.load("images/Close.png").convert_alpha(), (64, 64))
    IMAGES["aiplay"] = p.transform.scale(p.image.load("images/AIPlay.png").convert_alpha(), (64, 64))
    IMAGES["playagain"] = p.transform.scale(p.image.load("images/NewGame.png").convert_alpha(), (64, 64))
    # IMAGES["resetturn"] = p.transform.scale(p.image.load("images/ResetTurn.png").convert_alpha(), (32, 32))

    for img in IMAGES.values():
        for x in range(img.get_size()[0]):
            for y in range(img.get_size()[1]):
                a = img.get_at((x, y))[3]
                img.set_at((x, y), p.Color(0, 0, 0, a))

    for unit in units:
        for team in range(2):
            # Load piece image at file location and add to dictionary
            img = p.image.load("images/" + str(team) + unit + ".png").convert_alpha()
            IMAGES[str(team) + unit] = p.transform.scale(img, (64, 64))

    for dice in range(1, 7):
        # Load piece image at file location and add to dictionary
        img = p.image.load("images/Dice" + str(dice) + ".png").convert_alpha()
        IMAGES["dice" + str(dice)] = p.transform.scale(img, (148, 148))


# Creates buttons and adds them to buttons list so that they can be called on mouse clicks
def set_buttons():
    Button("Main", 20, 20, 40, 40, "New Game", p.Color(180, 180, 180), p.Color(100, 100, 100), new_game)
    Button("Main", 20, 70, 40, 40, "Settings", p.Color(180, 180, 180), p.Color(100, 100, 100), change_menu, "Settings")
    Button("Main", 980, 560, 216, 64, "End Turn", p.Color(180, 180, 180), p.Color(100, 100, 100), end_turn)
    Button("Main", 84, 560, 216, 64, "AI Play", p.Color(180, 180, 180), p.Color(100, 100, 100), end_turn, [True])
    Button("Settings", 558, 560, 164, 64, "Close", p.Color(180, 180, 180), p.Color(100, 100, 100), change_menu, "Main")
    Button("EndGame", 980, 560, 216, 64, "Play Again", p.Color(180, 180, 180), p.Color(100, 100, 100), new_game)
    # Button("Main", 20, 120, 40, 40, "Reset Turn", p.Color(180, 180, 180), p.Color(100, 100, 100), None)


# Actions that are called to draw the UI onto the display
def draw_game():
    # Note: Graphics that are drawn first will be placed in the "background" (they will be drawn over)
    # Fill in background
    SCREEN.fill(p.Color("white"))
    # Draw main menu
    if CURRENT_MENU != "Settings":
        # Draw the chess board
        draw_squares()
        # Draw the locations that the selected piece can move
        draw_moves()
        # Draw the pieces
        draw_pieces()
        # Draw the dice
        draw_dice()

    # Draw the buttons
    draw_buttons()
    # Draw the text
    draw_text()
    # Draw the tooltip on the mouse
    draw_tooltip()
    # Refresh the display
    p.display.flip()


def change_menu(new_menu):
    global CURRENT_MENU

    CURRENT_MENU = new_menu


def draw_squares():
    # Colors of the squares
    colors = [p.Color("white"), p.Color("gray")]
    # The border surrounding the chess board
    p.draw.rect(SCREEN, p.Color("black"), p.Rect(OFFSET[0] - 5, OFFSET[1] - 5, WIDTH + 10, HEIGHT + 10))

    for x in range(DIMENSION):
        for y in range(DIMENSION):
            # Checkerboard pattern
            color = colors[(x + y) % 2]
            # Draw square at position
            s = p.draw.rect(SCREEN, color, p.Rect(x * SQ_SIZE + OFFSET[0], y * SQ_SIZE + OFFSET[1], SQ_SIZE, SQ_SIZE))
            # Add squares to list so that they can be referenced
            # Occurs only in first iteration
            if len(SQUARES) <= pow(DIMENSION, 2):
                SQUARES.append((s, x, y))


def draw_moves():
    # Skip if no piece is currently selected
    if PIECE is not None:
        # [Light move color, dark move color, light attack color, dark attack color]
        colors = [p.Color(100, 255, 255), p.Color(0, 200, 200), p.Color(255, 100, 100), p.Color(200, 0, 0), p.Color(100, 255, 100), p.Color(0, 200, 0)]

        for x in range(DIMENSION):
            for y in range(DIMENSION):
                # Check if square at [y, x] is in list of moves or attacks for piece
                if [y, x] in MOVE_LIST:
                    p.draw.rect(SCREEN, colors[(x + y) % 2], p.Rect(x * SQ_SIZE + OFFSET[0], y * SQ_SIZE + OFFSET[1], SQ_SIZE, SQ_SIZE))
                elif [y, x] in ATTACK_LIST:
                    p.draw.rect(SCREEN, colors[(x + y) % 2 + 2], p.Rect(x * SQ_SIZE + OFFSET[0], y * SQ_SIZE + OFFSET[1], SQ_SIZE, SQ_SIZE))
                elif [y, x] == PIECE_COORDS:
                    p.draw.rect(SCREEN, colors[(x + y) % 2 + 4], p.Rect(x * SQ_SIZE + OFFSET[0], y * SQ_SIZE + OFFSET[1], SQ_SIZE, SQ_SIZE))


def draw_pieces():
    del_color = {"K": (0, 0, 255), "L": (0, 255, 0), "R": (255, 0, 0)}
    white_count = 0
    black_count = 0

    for x in range(DIMENSION):
        for y in range(DIMENSION):
            # Get piece at position on board
            piece = BOARD.board[y][x]
            # Check if piece at position
            if piece is not None:
                # Get correct image from the image dictionary and draw at position
                img_name = str(piece.team) + piece.unit
                SCREEN.blit(IMAGES[img_name], p.Rect(x * SQ_SIZE + OFFSET[0], y * SQ_SIZE + OFFSET[1], SQ_SIZE, SQ_SIZE))
                p.draw.rect(SCREEN, p.Color(del_color[piece.delegation]), p.Rect(x * SQ_SIZE + OFFSET[0] + 2, (y + 1) * SQ_SIZE + OFFSET[1] - 4, 60, 4))

    # Draw captured pieces
    for piece in BOARD.captured:
        img_name = str(piece.team) + piece.unit
        img = p.transform.scale(IMAGES[img_name], (32, 32))
        if piece.team == 0:
            SCREEN.blit(img, p.Rect(white_count % 4 * 32 + 64, white_count // 4 * 32 + 280, SQ_SIZE, SQ_SIZE))
            white_count += 1
        else:
            SCREEN.blit(img, p.Rect((black_count % 4 + 4) * 32 + 64, black_count // 4 * 32 + 280, SQ_SIZE, SQ_SIZE))
            black_count += 1


def draw_buttons():
    # Draw each button to the display
    for b in BUTTONS:
        if b.context == CURRENT_MENU:
            b.draw_button()


def draw_text():
    # Spacing between each line in the moves list
    spacing = 0
    # Text objects (headers) that will be rendered (Text, x-position, y-position, font size)
    if CURRENT_MENU != "Settings":
        text_objects = [("Medieval Fuzzy Logic Chess", 640, 50, 40), ("Dice Roll:", 1088, 320, 32), ("Moves:", 1088, 64, 32), ("Pieces Captured:", 192, 250, 32)]
        if CURRENT_MENU == "EndGame":
            text_objects.append(("GAME OVER:", 192, 500, 32))
            text_objects.append((TEAM[BOARD.state] + " Team Wins!", 192, 550, 32))
    else:
        text_objects = [("Settings", 640, 50, 40)]

    for text in text_objects:
        # Get system font (font name, font size, bold=false, italic=false)
        text_font = p.font.SysFont("Calibri", text[3], True)
        # Add underline to text
        text_font.set_underline(True)
        # Actual text object that will be rendered
        text_obj = text_font.render(text[0], True, p.Color("black"))
        # Get dimensions of the text object so that it can be centered
        text_size = text_obj.get_size()
        # Render the text
        SCREEN.blit(text_obj, (text[1] - text_size[0] / 2, text[2] - text_size[1] / 2))

    if PROCESSING:
        text_font = p.font.SysFont("Calibri", 32, True)
        text_obj = text_font.render("Thinking" + ((p.time.get_ticks() // 1000 % 3 + 1) * "."), True, p.Color("black"))
        text_size = text_obj.get_size()
        SCREEN.blit(text_obj, (640 - text_size[0] / 2, 670 - text_size[1] / 2))

    if CURRENT_MENU != "Settings":
        for move in MOVES:
            for text in move:
                is_header = text == "" or text[-1] == ":"
                text_font = p.font.SysFont("Calibri", 18, is_header)
                text_font.set_underline(is_header)
                text_obj = text_font.render(text, True, p.Color("black"))
                text_size = text_obj.get_size()
                SCREEN.blit(text_obj, (1088 - text_size[0] / 2, 100 - text_size[1] / 2 + spacing))
                # Add spacing between text ("newline")
                spacing += text_size[1] + 5
            # Add spacing between text ("return")
            spacing += 5


def draw_dice():
    # Get dice with number DICE_ROLL and render to display
    SCREEN.blit(IMAGES["dice" + str(DICE_ROLL)], p.Rect(1014, 370, 148, 148))


def draw_tooltip():
    if len(TOOLTIP) != 0:
        # Spacing between each line of text
        spacing = 0
        # The size of the rect object
        # Starts at [0, 4] to give height padding
        dimensions = [0, 4]
        # Font of the tooltip's text
        text_font = p.font.SysFont("Calibri", 20, False, True)

        # For loop to get the max width and total height of the text
        # If the text is rendered here, it will get drawn over by the rect
        for text in TOOLTIP:
            text_obj = text_font.render(text, True, p.Color("black"))
            text_size = text_obj.get_size()
            if dimensions[0] < text_size[0]:
                dimensions[0] = text_size[0] + 8
            dimensions[1] += text_size[1] + 5

        # Draw tooltip and its border using dimensions found by for loop
        p.draw.rect(SCREEN, p.Color(240, 240, 240), p.Rect(MOUSE_POS[0] + 8, MOUSE_POS[1] + 8, dimensions[0] + 4, dimensions[1] + 4))
        p.draw.rect(SCREEN, p.Color("white"), p.Rect(MOUSE_POS[0] + 10, MOUSE_POS[1] + 10, dimensions[0], dimensions[1]))

        # Render each string in tooltip list
        for text in TOOLTIP:
            text_obj = text_font.render(text, True, p.Color("black"))
            SCREEN.blit(text_obj, (MOUSE_POS[0] + 14, MOUSE_POS[1] + spacing + 14))
            spacing += text_obj.get_size()[1] + 5


def update_moves(action=-1, start_pos=[], end_pos=[], roll=DICE_ROLL):
    global MOVES

    del_index = {"K": 0, "L": 1, "R": 2}
    del_name = {"K": "King", "L": "Left", "R": "Right"}

    if len(MOVES) != 3 and PIECE.team == 0:
        MOVES = [["King:"], ["Left:"], ["Right:"]]

    # Check if piece exists
    if PIECE is not None:
        # Get delegation of the piece and the corresponding index of the moves list
        delegation = PIECE.delegation
        move_list = MOVES[del_index[delegation]]

        # Move action
        if action == 0:
            if len(move_list) != 1:
                move_list[len(move_list) - 1] += " and"
                move_list.append("moved " + get_notation(start_pos) + " to " + get_notation(end_pos))
            else:
                move_list.append("Moved " + get_notation(start_pos) + " to " + get_notation(end_pos))
        # Successful attack action
        elif action == 1:
            # Check if this piece is a knight attacking after moving
            if PIECE.unit == "n" and len(move_list) != 1:
                move_list[len(move_list) - 1] += " and"
                move_list.append("attacked " + get_notation(end_pos) + " (" + str(roll) + ")")
            else:
                move_list.append(get_notation(start_pos) + " attacked " + get_notation(end_pos) + " (" + str(roll) + ")")
        # Unsuccessful attack action
        elif action == 2:
            # Check if this piece is a knight attacking after moving
            if PIECE.unit == "n" and len(move_list) != 1:
                move_list[len(move_list) - 1] += " and"
                move_list.append("failed to attack " + get_notation(end_pos) + " (" + str(roll) + ")")
            else:
                move_list.append(get_notation(start_pos) + " failed to attack " + get_notation(end_pos) + " (" + str(roll) + ")")
        # Delegate action
        elif action == 3:
            if len(move_list) != 1:
                move_list[len(move_list) - 1] += " and"
                move_list.append("delegated " + get_notation(start_pos) + " to " + del_name[BOARD.get_piece(end_pos).delegation])
            else:
                move_list.append("Delegated " + get_notation(start_pos) + " to " + del_name[BOARD.get_piece(end_pos).delegation])


def mouse_event(event):
    global PIECE, PIECE_COORDS, MOVE_LIST, ATTACK_LIST, MOUSE_POS, TOOLTIP

    # Clear tooltip list
    TOOLTIP = []
    # Get the mouse's position
    MOUSE_POS = p.mouse.get_pos()
    # Check if mouse is over a square on the chess board or a button
    selected_square = [s for s in SQUARES if s[0].collidepoint(MOUSE_POS)]
    selected_button = [b for b in BUTTONS if b.rect.collidepoint(MOUSE_POS) and b.context == CURRENT_MENU]

    # Get the column and row on chess board
    if len(selected_square) != 0:
        col = selected_square[0][2]
        row = selected_square[0][1]
        coords = [col, row]

    # Check if mouse button is being pressed
    if event.type == p.MOUSEBUTTONDOWN and not PROCESSING:
        # If on chess board
        if len(selected_square) != 0 and CURRENT_MENU == "Main":
            # If selected piece does not exists
            if len(PIECE_COORDS) == 0:
                # If piece exists at location and is player's piece
                if BOARD.board[col][row] is not None and BOARD.get_piece(coords).team == 0 and BOARD.get_piece(coords).attack:
                    # Cache piece and its coordinates
                    PIECE_COORDS = coords
                    PIECE = BOARD.get_piece(PIECE_COORDS)
                    MOVE_LIST = BOARD.get_moves(PIECE_COORDS)
                    ATTACK_LIST = BOARD.get_attacks(PIECE_COORDS)
            else:
                # Left mouse click
                if event.button == 1:
                    # If piece exists at location and is player's piece
                    if BOARD.board[col][row] is not None and BOARD.get_piece(coords).team == 0 and BOARD.get_piece(coords).attack:
                        # Cache piece and its coordinates
                        PIECE_COORDS = coords
                        PIECE = BOARD.get_piece(PIECE_COORDS)
                        MOVE_LIST = BOARD.get_moves(PIECE_COORDS)
                        ATTACK_LIST = BOARD.get_attacks(PIECE_COORDS)
                        # Return so that values aren't overwritten
                        return
                    else:
                        # Move piece to new position
                        move_piece(coords)
                # Right mouse click
                elif event.button == 3:
                    # Attack piece at position
                    attack_piece(coords)
                # Middle mouse click
                elif event.button == 2:
                    # Change piece's delegation
                    delegate_piece(coords)
                elif event.button == 6:
                    AI.test_future_move()
                    # AI.previous = []
                    # print(AI.future_move(PIECE_COORDS, BOARD, PIECE_COORDS, 0))
                    # print((AI.corps[BOARD.get_piece(PIECE_COORDS).delegation].get_future_moves()))
                    # AI.testing_stuff()
                # Reset piece
                if not IS_ROLLING:
                    PIECE_COORDS = []
                    PIECE = None
                    MOVE_LIST = []
                    ATTACK_LIST = []
        # If left-click on button
        elif len(selected_button) != 0 and event.button == 1 and selected_button[0].func is not None:
            # Call action on button
            if len(selected_button[0].params) == 0:
                selected_button[0].func()
            else:
                selected_button[0].func(selected_button[0].params)

    # Hover events
    # If on chess board
    if len(selected_square) != 0 and CURRENT_MENU == "Main":
        # If selected piece exists
        if PIECE is not None:
            # Get location on board in chess notation
            TOOLTIP.append(get_notation(coords))
            # If selected piece can move to square's position
            if coords in MOVE_LIST:
                TOOLTIP.append("Left-click to move")
            # If selected piece can attack square's position
            elif coords in ATTACK_LIST:
                TOOLTIP.append("Right-click to attack")
                TOOLTIP.append("Chance of success: " + str(get_success_rate(PIECE_COORDS, coords)) + " / 6")
            # If square's position is the selected piece's position
            elif coords == PIECE_COORDS:
                piece_info = piece_to_string(BOARD.get_piece(coords))
                TOOLTIP = [get_notation(coords) + ": " + piece_info[0], piece_info[1]]
            # If square has piece on it that isn't selected piece and can be selected
            elif BOARD.get_piece(coords) is not None and BOARD.get_piece(coords).team == 0 and BOARD.get_piece(coords).attack:
                piece_info = piece_to_string(BOARD.get_piece(coords))
                TOOLTIP = [get_notation(coords) + ": " + piece_info[0], piece_info[1], "Left-click to select"]
                if BOARD.get_piece(coords).delegation != "K" and PIECE.delegation == "K":
                    TOOLTIP.append("Middle-click to change delegation")
            # If square has piece whose delegation has already played
            elif BOARD.get_piece(coords) is not None:
                piece_info = piece_to_string(BOARD.get_piece(coords))
                TOOLTIP = [get_notation(coords) + ": " + piece_info[0], piece_info[1], "Click to cancel"]
            # Empty square on chess board
            else:
                TOOLTIP.append("Click to cancel")
        # If no selected piece and square has a piece on it
        elif BOARD.get_piece(coords) is not None:
            piece_info = piece_to_string(BOARD.get_piece(coords))
            # If square has team piece on it
            if BOARD.get_piece(coords).team == 0:
                # If square has piece whose delegation has already played
                if BOARD.get_piece(coords).attack:
                    TOOLTIP = [get_notation(coords) + ": " + piece_info[0], piece_info[1], "Left-click to select"]
                else:
                    TOOLTIP = [get_notation(coords) + ": " + piece_info[0], piece_info[1], "Can't be selected"]
            # If square has enemy piece on it (exclude left-click options prompt)
            else:
                TOOLTIP = [get_notation(coords) + ": " + piece_info[0], piece_info[1]]
        # Empty square on chess board
        else:
            # Get location on board in chess notation
            TOOLTIP.append(get_notation(coords))
    # If over button
    elif len(selected_button) != 0:
        # Show button text
        TOOLTIP.append(selected_button[0].text)


def move_piece(coords):
    # Perform move action and check if move actually occurs
    if BOARD.move(PIECE_COORDS, coords):
        # Add move action to moves list
        update_moves(0, PIECE_COORDS, coords)


def attack_piece(coords):
    global DICE_THREAD

    # Start thread that will perform the attack action
    DICE_THREAD = threading.Thread(target=randomize_dice, args=[coords])
    DICE_THREAD.start()


def delegate_piece(coords):
    # Check if valid delegation change
    if PIECE.team == BOARD.get_piece(coords).team and PIECE.delegation == "K" and PIECE.unit != "k":
        # Perform delegation change action
        BOARD.del_piece(PIECE_COORDS, BOARD.get_piece(coords).delegation)
        # Add action to moves list
        update_moves(3, PIECE_COORDS, coords)


def randomize_dice(coords):
    global PIECE_COORDS, PIECE, MOVE_LIST, ATTACK_LIST, DICE_ROLL, DICE_THREAD, IS_ROLLING

    IS_ROLLING = True
    # Update dice roll number to update dice image
    for _ in range(16):
        DICE_ROLL = random.randint(1, 6)
        time.sleep(0.0625)

    # Perform attack action
    roll = BOARD.attack(PIECE_COORDS, coords)

    DICE_ROLL = roll[1]
    # Check if attack was valid
    if roll[1] != 0:
        # Check if attack was successful and add action to moves list
        if roll[0] == 1:
            # Success
            update_moves(1, PIECE_COORDS, coords)
        else:
            # Failure
            update_moves(2, PIECE_COORDS, coords)

    PIECE_COORDS = []
    PIECE = None
    MOVE_LIST = []
    ATTACK_LIST = []

    DICE_THREAD = False
    IS_ROLLING = False

# Returns the coordinate on the chess board in chess notation (e.g. [0, 0] -> "A1")
def get_notation(coords):
    letters = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
    return letters[coords[1]] + str(8 - coords[0])


# Returns piece info in a format useful to the tooltip
def piece_to_string(piece):
    return TEAM[piece.team] + " " + UNIT[piece.unit], "Delegation: " + DELEGATION[piece.delegation]


# Returns the success rate of an attack on defender by attacker as an integer
def get_success_rate(attacker, defender):
    if BOARD.get_piece(attacker).unit == "n" and not BOARD.get_piece(attacker).move:
        return 6 - BOARD.attack_values[BOARD.get_piece(attacker).unit + BOARD.get_piece(defender).unit]
    return 7 - BOARD.attack_values[BOARD.get_piece(attacker).unit + BOARD.get_piece(defender).unit]


# Object definition for handing buttons
class Button:
    # Class constructor
    # context -> the display that the button will work on
    # (x, y) -> coordinates of the top-left corner of the button
    # (w, h) -> width and height of the button
    # text -> text displayed on the button
    # color -> the background color of the button
    # action -> the event that is called when the button is clicked
    def __init__(self, context, x, y, w, h, text, color, select_color, func, params=[]):
        self.context = context
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.color = color
        self.select_color = select_color
        self.rect = p.draw.rect(SCREEN, self.color, [self.x, self.y, self.w, self.h])
        self.func = func
        self.params = params
        # Adds the button to the buttons list (required for mouse clicks to work)
        BUTTONS.append(self)

    # Draws the button onto the display
    def draw_button(self):
        # Draw the border of the button
        p.draw.rect(SCREEN, p.Color("black"), [self.x - 2, self.y - 2, self.w + 4, self.h + 4])
        # Draw the main rect object of the button
        if self.x < MOUSE_POS[0] < self.x + self.w and self.y < MOUSE_POS[1] < self.y + self.h:
            self.rect = p.draw.rect(SCREEN, self.select_color, [self.x, self.y, self.w, self.h])
        else:
            self.rect = p.draw.rect(SCREEN, self.color, [self.x, self.y, self.w, self.h])
        img = IMAGES[self.text.replace(" ", "").lower()]

        # Draw the text onto the end turn button
        if self.text in ["End Turn", "Close", "Play Again", "AI Play"]:
            text_font = p.font.SysFont("Calibri", 32)
            text_obj = text_font.render(self.text, True, p.Color("black"))
            text_size = text_obj.get_size()
            SCREEN.blit(text_obj, (self.x + 80, self.y + self.h / 2 - text_size[1] / 2))
            SCREEN.blit(img, p.Rect(self.x + 4, self.y, img.get_size()[0], img.get_size()[1]))
        else:
            SCREEN.blit(img, p.Rect(self.x + 4, self.y + 4, 32, 32))


if __name__ == '__main__':
    main()
