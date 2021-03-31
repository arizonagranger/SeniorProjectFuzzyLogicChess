## controls: left mouse move, right mouse attack, middle mouse delegate, any key ends turn

import pygame as p
from Board import Board
from RandomAI import RandomAI

p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def load_images():
    units = ["a","i","p","q","k","n"]
    corps = ["L","K","R"]
    for unit in units:
        for corp in corps:
            for team in range(2):
                IMAGES[str(team)+unit+corp] = p.transform.scale(p.image.load("images/"+str(team)+unit+corp+".png"), (SQ_SIZE, SQ_SIZE))



def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("chess")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    board = Board("WAKNRPRQKKKPLNLAKIRIRIRIKIKILILIL32iLiLiLiKiKiRiRiRaKnLpLqKkKpRnRaK")
    a = RandomAI(board, 1)
    load_images()
    game_exit = False
    piece_selected = []
    while not game_exit:
        for event in p.event.get():
            if event.type == p.QUIT:
                game_exit = True
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[1]//SQ_SIZE
                row = location[0]//SQ_SIZE
                if len(piece_selected) == 0 and board.board[col][row] is not None:
                    piece_selected = [col, row]
                elif len(piece_selected) != 0 and event.button == 1:
                    board.move(piece_selected, [col, row])
                    piece_selected = []
                elif len(piece_selected) != 0 and event.button == 3:
                    print("human: ", board.attack(piece_selected, [col, row]))
                    piece_selected = []
                elif len(piece_selected) != 0 and event.button == 2:
                    board.del_piece(piece_selected, board.board[col][row].delegation)
                    piece_selected = []
            elif event.type == p.KEYDOWN:
                board.end_turn()
        if len(piece_selected) == 0:
            p.display.set_caption("select a piece")
        else:
            p.display.set_caption(str(piece_selected)+": selected")
        if board.turn == 1:
            a.ai_move()
        draw_game(screen, board)
        clock.tick(MAX_FPS)
        p.display.flip()
    p.quit()
    quit()


def draw_game(screen, board):
    draw_squares(screen)
    draw_pieces(screen, board)


def draw_squares(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            color = colors[((x+y)%2)]
            p.draw.rect(screen, color, p.Rect(y*SQ_SIZE, x*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for x in range(DIMENSION):
        for y in range(DIMENSION):
            piece = board.board[x][y]
            if piece is not None:
                screen.blit(IMAGES[str(piece.team) + piece.unit + piece.delegation], p.Rect(y*SQ_SIZE, x*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
