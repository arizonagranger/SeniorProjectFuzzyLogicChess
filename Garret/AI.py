from Board import Board
import random

class AI:

    def __init__(self, board, team):
        self.team = team
        self.board = board
        self.board_strings = []
        self.board_strings.append(board.get_board())
        self.corps = [[], [], []]
        self.update_corps()

    def update_corps(self):
        self.corps = [[], [], []]
        symbols = ["L", "K", "R"]
        for x in range(len(symbols)):
            self.corps[x] = self.board.get_del(self.team, symbols[x])

    def ai_move(self):
        print("attacks:", self.ai_rand_attack())
        print("moves: ", self.ai_rand_move())
        self.board.end_turn()

    def ai_rand_move(self):
        rand_corps = random.sample(self.corps, len(self.corps))
        moves = {}
        results = {}
        for corp in rand_corps:
            for piece in corp:
                if len(self.board.get_moves(piece)) > 0:
                    moves[(str(piece[0])+str(piece[1]))] = self.board.get_moves(piece)
            if len(list(moves)) > 0:
                move = random.choice(list(moves))
                location = random.choice(moves[str(move)])
                results[str([int(move[0]), int(move[1])])] = location
                self.board.move([int(move[0]), int(move[1])], location)
        self.update_corps()
        return results

    def ai_rand_attack(self):
        rand_corps = random.sample(self.corps, len(self.corps))
        attacks = {}
        results = []
        for corp in rand_corps:
            for piece in corp:
                if len(self.board.get_attacks(piece)) > 0:
                    attacks[(str(piece[0])+str(piece[1]))] = self.board.get_attacks(piece)
            if len(list(attacks)) > 0:
                attack = random.choice(list(attacks))
                results.append(self.board.attack([int(attack[0]), int(attack[1])], random.choice(attacks[str(attack)])))
        self.update_corps()
        return results


