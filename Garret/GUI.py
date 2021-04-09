import pygame as p
import Board as Board
import RandomAI as RandAI
import random

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
INITIAL_STATE = "WAKNRPRQKKKPLNLAKIRIRIRIKIKILILIL32iLiLiLiKiKiRiRiRaKnLpLqKkKpRnRaK"
# Board object reference
BOARD = Board.Board(INITIAL_STATE)
# Create the main window display using the screen size
SCREEN = p.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
# AI object reference
AI = RandAI.RandomAI(BOARD, 1)
# The currently selected chess piece; none if no piece is selected
PIECE = None
# The value of the last dice roll; 0 on start
DICE_ROLL = 0
# The list of strings that will appear in the tooltip object; empty on start
# Made as a list of strings since pygame doesn't support multi-line text
TOOLTIP = []

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
MOVES = [["King: "], ["Left Bishop: "], ["Right Bishop: "]]

# Dictionaries for replacing piece attributes with readable text
TEAM = {0: "White", 1: "Black"}
UNIT = {"a": "Rook", "i": "Pawn", "k": "King", "n": "Knight", "p": "Bishop", "q": "Queen"}
DELEGATION = {"K": "King", "L": "Left Bishop", "R": "Right Bishop"}

# Boolean that checks whether the game state is currently running
GAME_RUNNING = True


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
    global BOARD, AI, DICE_ROLL, GAME_RUNNING

    # Reset the board state
    BOARD = Board.Board(INITIAL_STATE)
    # Reset the AI
    AI = RandAI.RandomAI(BOARD, 1)
    # Sets the dice to a random number
    DICE_ROLL = random.randint(1, 6)
    # Clear captured pieces list
    CAPTURED_PIECES = []
    # Set game running to true
    GAME_RUNNING = True

    # Reset other stats
    reset_state()

# Actions that occur every frame
def update_game():
    global GAME_RUNNING

    # Draw UI graphics onto display
    draw_game()

    # Check if any events occur during frame
    for event in p.event.get():
        # p.QUIT is called when the application closes
        if event.type == p.QUIT:
            GAME_RUNNING = False
        # Check for mouse events (clicks, hovering, etc.)
        mouse_event(event)

    # Do AI actions if not the player's turn
    if BOARD.turn == 1:
        AI.ai_move()


# Actions that occur when the player ends their turn
def end_turn():
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
    MOVES = [["King: "], ["Left Bishop: "], ["Right Bishop: "]]


# Actions that occur when the program is quitting
def quit_game():
    # End pygame session
    p.quit()
    # End Python program
    quit()


# Loads images from file location into dictionary (for performance reasons)
def load_images():
    # Piece images are formatted as: (team + unit + corp).png
    # Dice images are formatted as: Dice(number).png
    units = ["a", "i", "p", "q", "k", "n"]

    # Load icons for buttons and add to dictionary
    IMAGES["newgame"] = p.transform.scale(p.image.load("images/NewGame.png").convert_alpha(), (32, 32))
    IMAGES["resetturn"] = p.transform.scale(p.image.load("images/ResetTurn.png").convert_alpha(), (32, 32))
    IMAGES["settings"] = p.transform.scale(p.image.load("images/Settings.png").convert_alpha(), (32, 32))
    IMAGES["endturn"] = p.transform.scale(p.image.load("images/EndTurn.png").convert_alpha(), (64, 64))

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
    Button(20, 20, 40, 40, "New Game", p.Color(180, 180, 180), p.Color(170, 170, 170), new_game)
    Button(20, 70, 40, 40, "Settings", p.Color(180, 180, 180), p.Color(170, 170, 170), None)
    Button(20, 120, 40, 40, "Reset Turn", p.Color(180, 180, 180), p.Color(170, 170, 170), None)
    Button(980, 560, 216, 64, "End Turn", p.Color(180, 180, 180), p.Color(170, 170, 170), end_turn)


# Actions that are called to draw the UI onto the display
def draw_game():
    # Note: Graphics that are drawn first will be placed in the "background" (they will be drawn over)
    # Fill in background
    SCREEN.fill(p.Color("white"))
    # Draw the chess board
    draw_squares()
    # Draw the locations that the selected piece can move
    draw_moves()
    # Draw the pieces
    draw_pieces()
    # Draw the buttons
    draw_buttons()
    # Draw the text
    draw_text()
    # Draw the dice
    draw_dice()
    # Draw the tooltip on the mouse
    draw_tooltip()
    # Refresh the display
    p.display.flip()


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
        colors = [p.Color(100, 255, 255), p.Color(0, 200, 200), p.Color(255, 100, 100), p.Color(200, 0, 0)]

        for x in range(DIMENSION):
            for y in range(DIMENSION):
                # Check if square at [y, x] is in list of moves or attacks for piece
                if [y, x] in MOVE_LIST:
                    p.draw.rect(SCREEN, colors[(x + y) % 2], p.Rect(x * SQ_SIZE + OFFSET[0], y * SQ_SIZE + OFFSET[1], SQ_SIZE, SQ_SIZE))
                elif [y, x] in ATTACK_LIST:
                    p.draw.rect(SCREEN, colors[(x + y) % 2 + 2], p.Rect(x * SQ_SIZE + OFFSET[0], y * SQ_SIZE + OFFSET[1], SQ_SIZE, SQ_SIZE))


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
        b.draw_button()


def draw_text():
    # Spacing between each line in the moves list
    spacing = 0
    # Text objects (headers) that will be rendered (Text, x-position, y-position, font size)
    text_objects = [("Medieval Fuzzy Logic Chess", 640, 50, 40), ("Dice Roll:", 1088, 320, 32),
                    ("Moves:", 1088, 128, 32), ("Pieces Captured:", 192, 250, 32)]

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

    for move in MOVES:
        for text in move:
            text_font = p.font.SysFont("Calibri", 20)
            text_obj = text_font.render(text, True, p.Color("black"))
            text_size = text_obj.get_size()
            SCREEN.blit(text_obj, (1088 - text_size[0] / 2, 160 - text_size[1] / 2 + spacing))
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


def update_moves(action=-1, start_pos=[], end_pos=[]):
    del_index = {"K": 0, "L": 1, "R": 2}
    del_name = {"K": "King", "L": "Left Bishop", "R": "Right Bishop"}

    # Check if piece exists
    if PIECE is not None:
        # Get delegation of the piece and the corresponding index of the moves list
        delegation = PIECE.delegation
        move_list = MOVES[del_index[delegation]]

        # Move action
        if action == 0:
            move_list[0] = del_name[delegation] + ": Moved " + str(start_pos) + " to " + str(end_pos)
        # Successful attack action
        elif action == 1:
            # Check if this piece is a knight attacking after moving
            if PIECE.unit == "n" and move_list[0] != "":
                move_list.append("and successfully attacked " + str(end_pos) + " (" + str(DICE_ROLL) + ")")
            else:
                move_list[0] = del_name[delegation] + ": " + str(start_pos) + " successfully attacked " + str(end_pos) + " (" + str(DICE_ROLL) + ")"
        # Unsuccessful attack action
        elif action == 2:
            # Check if this piece is a knight attacking after moving
            if PIECE.unit == "n" and move_list[0] != "":
                move_list.append("and failed to attack " + str(end_pos) + " (" + str(DICE_ROLL) + ")")
            else:
                move_list[0] = del_name[delegation] + ": " + str(start_pos) + " failed to attack " + str(end_pos) + " (" + str(DICE_ROLL) + ")"
        # Delegate action
        elif action == 3:
            move_list[0] = del_name[delegation] + ": Delegate"


def mouse_event(event):
    global PIECE, PIECE_COORDS, MOVE_LIST, ATTACK_LIST, MOUSE_POS, TOOLTIP

    # Clear tooltip list
    TOOLTIP = []
    # Get the mouse's position
    MOUSE_POS = p.mouse.get_pos()
    # Check if mouse is over a square on the chess board or a button
    selected_square = [s for s in SQUARES if s[0].collidepoint(MOUSE_POS)]
    selected_button = [b for b in BUTTONS if b.rect.collidepoint(MOUSE_POS)]

    # Get the column and row on chess board
    if len(selected_square) != 0:
        col = selected_square[0][2]
        row = selected_square[0][1]
        coords = [col, row]

    # Check if mouse button is being pressed
    if event.type == p.MOUSEBUTTONDOWN:
        # If on chess board
        if len(selected_square) != 0:
            # If selected piece does not exists
            if len(PIECE_COORDS) == 0:
                # If piece exists at location and is player's piece
                if BOARD.board[col][row] is not None and BOARD.get_piece(coords).team == 0 and BOARD.get_piece(coords).attack == True:
                    # Cache piece and its coordinates
                    PIECE_COORDS = coords
                    PIECE = BOARD.get_piece(PIECE_COORDS)
                    MOVE_LIST = BOARD.get_moves(PIECE_COORDS)
                    ATTACK_LIST = BOARD.get_attacks(PIECE_COORDS)
            else:
                # Left mouse click
                if event.button == 1:
                    # If piece exists at location and is player's piece
                    if BOARD.board[col][row] is not None and BOARD.get_piece(coords).team == 0 and BOARD.get_piece(coords).attack == True:
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
                # Reset piece
                PIECE_COORDS = []
                PIECE = None
                MOVE_LIST = []
                ATTACK_LIST = []
        # If left-click on button
        elif len(selected_button) != 0 and event.button == 1:
            # Call action on button
            selected_button[0].action()

    # Hover events
    # If on chess board
    if len(selected_square) != 0:
        # If selected piece exists
        if PIECE is not None:
            # Get location on board in chess notation
            TOOLTIP.append(get_notation(coords))
            # If selected piece can move to square's position
            if coords in BOARD.get_moves(PIECE_COORDS):
                TOOLTIP.append("Left-click to move")
            # If selected piece can attack square's position
            elif coords in BOARD.get_attacks(PIECE_COORDS):
                TOOLTIP.append("Right-click to attack")
                TOOLTIP.append("Chance of success: " + str(get_success_rate(PIECE_COORDS, coords)) + " / 6")
            # If square's position is the selected piece's position
            elif coords == PIECE_COORDS:
                TOOLTIP.append("Middle-click to change delegation")
            # If square has piece on it that isn't selected piece and can be selected
            elif BOARD.get_piece(coords) is not None and BOARD.get_piece(coords).team == 0 and BOARD.get_piece(coords).attack == True:
                piece_info = piece_to_string(BOARD.get_piece(coords))
                TOOLTIP = [get_notation(coords) + ": " + piece_info[0], piece_info[1], "Left-click to select"]
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
                if BOARD.get_piece(coords).attack == True:
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
    global DICE_ROLL

    # Perform attack action
    roll = BOARD.attack(PIECE_COORDS, coords)

    # Check if attack was valid
    if roll[1] != 0:
        # Update dice roll number to update dice image
        DICE_ROLL = roll[1]
        # Check if attack was successful and add action to moves list
        if roll[0] == 1:
            # Success
            update_moves(1, PIECE_COORDS, coords)
        else:
            # Failure
            update_moves(2, PIECE_COORDS,  coords)


def delegate_piece(coords):
    # Perform delegation change action
    BOARD.del_piece(PIECE_COORDS, BOARD.board[coords[0]][coords[1]].delegation)
    # Add action to moves list
    update_moves(3, PIECE_COORDS, coords)


# Returns the coordinate on the chess board in chess notation (e.g. [0, 0] -> "A1")
def get_notation(coords):
    letters = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
    return letters[coords[1]] + str(8 - coords[0])


# Returns piece info in a format useful to the tooltip
def piece_to_string(piece):
    return TEAM[piece.team] + " " + UNIT[piece.unit], "Delegation: " + DELEGATION[piece.delegation]


# Returns the success rate of an attack on defender by attacker as an integer
def get_success_rate(attacker, defender):
    return 7 - BOARD.attack_values[BOARD.get_piece(attacker).unit + BOARD.get_piece(defender).unit]


# Object definition for handing buttons
class Button:
    # Class constructor
    # (x, y) -> coordinates of the top-left corner of the button
    # (w, h) -> width and height of the button
    # text -> text displayed on the button
    # color -> the background color of the button
    # action -> the event that is called when the button is clicked
    def __init__(self, x, y, w, h, text, color, select_color, action):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.color = color
        self.select_color = select_color
        self.action = action
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
        if self.text == "End Turn":
            text_font = p.font.SysFont("Calibri", 32)
            text_obj = text_font.render(self.text, True, p.Color("black"))
            text_size = text_obj.get_size()
            SCREEN.blit(text_obj, (self.x + 80, self.y + self.h / 2 - text_size[1] / 2))
            SCREEN.blit(img, p.Rect(self.x + 4, self.y, img.get_size()[0], img.get_size()[1]))
        else:
            SCREEN.blit(img, p.Rect(self.x + 4, self.y + 4, 32, 32))


if __name__ == '__main__':
    main()
