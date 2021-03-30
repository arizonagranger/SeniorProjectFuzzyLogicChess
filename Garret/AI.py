from Board import Board
import random


class AI:

    def __init__(self, board, team, corp="K"):
        self.piece_value = {"k": 1000, "p": 500, "q": 200, "a": 200, "n": 150, "i": 50}
        self.offense = random.uniform(0.5, 1.5)
        self.defense = 1 - self.offense
        self.team = team
        self.board = board
        self.board_strings = [board.get_board()]
        self.corp = corp
        if corp == "K":
            self.corps = {"L": AI(board, team, "L"), "R": AI(board, team, "R")}
        self.pieces = self.board.get_del(self.team, self.corp)

    def update_corp(self):
        temp = [x for x in self.pieces if self.board.get_piece(x.coord) is not None]
        self.pieces = temp

    def check_status(self, corp):
        self.update_corp()
        return len(self.corps[corp].pieces)

    def change_aggression(self):
        for corp in self.corps:
            if self.check_status(corp) / len(self.board.get_team(self.team)) > 0.3:
                corp.offense += 0.5
            elif self.check_status(corp) / len(self.board.get_team(self.team)) < 0.15 and len(
                    self.check_status(self.corp)) > 3:
                corp.defense += 0.5
            print("here")

    def scan_threats(self):
        self.update_corp()
        threats = {}
        temp = Board(self.board.get_board())
        temp.end_turn()
        for piece in temp.get_team(abs(1-self.team)):
            for attacks in temp.get_attacks(piece):
                if temp.get_piece(attacks) in self.pieces:
                    threats[self.move_value(piece, attacks)] += [piece, attacks]
        return threats

    def scan_for_targets(self):
        self.update_corp()
        temp = Board(self.board.get_board())
        temp.end_turn()
        attacks = {}
        for piece in self.pieces:
            for defender in temp.get_attacks(piece):
                attacks[self.move_value(piece, defender)] = [piece, defender]
        return attacks

    def update_corp(self):
        temp = [x for x in self.pieces if self.board.get_piece(x.coord) is not None]
        self.pieces = temp

    def move_value(self, attacker, defender):
        value = self.piece_value[self.board.get_piece(defender).unit] * \
               (1 - ((self.board.attack_values[
                          self.board.get_piece(attacker).unit + self.board.get_piece(defender).unit] - 1) / 6))
        if self.board.get_piece(attacker).team == self.team:
            return self.offense * value
        else:
            return -self.defense * value

    def ai_move(self):
        threats = self.scan_threats()
        targets = self.scan_for_targets()
        for corp in self.corps:
            threats += corp.scan_threats()
            targets += corp.scan_for_targets()

