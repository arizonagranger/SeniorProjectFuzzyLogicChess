from Board import Board
import random
from RandomAI import RandomAI


class AI:

    def __init__(self, board, team, corp="K"):
        self.piece_value = {"k": 1000, "p": 500, "q": 200, "a": 400, "n": 150, "i": 50}
        self.offense = random.uniform(0.5, 1.5)
        self.defense = 1 - self.offense
        self.team = team
        self.board = board
        self.board_strings = [board.get_board()]
        self.corp = corp
        if corp == "K":
            self.corps = {"L": AI(board, team, "L"), "R": AI(board, team, "R")}
        self.pieces = self.board.get_del(self.team, self.corp)

    #check how many pieces are left in the corp
    def check_status(self, corp):
        self.update_corp()
        return len(self.corps[corp].pieces)

    #alters the offense or defense based on the amount of pieces
    def change_aggression(self):
        for corp in self.corps:
            if self.check_status(corp) / len(self.board.get_team(self.team)) > 0.3:
                corp.offense += 0.5
            elif self.check_status(corp) / len(self.board.get_team(self.team)) < 0.15 and len(
                    self.check_status(self.corp)) > 3:
                corp.defense += 0.5

    #finds the king and returns true if its in danger
    def king_threat(self):
        for x in self.pieces:
            if self.board.get_piece(x).unit == "k":
                return self.scan_threats_for(x.coord)
        return False

    #checks if there are any threats on the given location
    def scan_threats_for(self, coord):
        if coord in self.board.get_attacks(coord):
            return True
        else:
            False

    #add all possible attacks into and array of two [whites level, blacks level]
    def scan_threat_level(self):
        temp = Board(self.board.get_board())
        threat_level = [0, 0]
        if temp.turn != 0:
            temp.end_turn()
        for x in range(2):
            for piece in temp.get_team(x):
                for attacks in temp.get_attacks(piece):
                    threat_level[x] += self.move_value(piece, attacks)
            temp.end_turn()
        return threat_level

    #returns a dictionary of value of the threat and the the pieces involved
    def scan_threats(self):
        self.update_corp()
        threats = {}
        temp = Board(self.board.get_board())
        for piece in temp.get_team(abs(1 - self.team)):
            for attacks in temp.get_attacks(piece):
                if temp.get_piece(attacks) in self.pieces:
                    threats[str(len(attacks)) + ":" + str(self.move_value(piece, attacks))] += [piece, attacks]
        return threats

    #checks all possible attacks
    def scan_for_targets(self):
        self.update_corp()
        temp = Board(self.board.get_board())
        attacks = {}
        for piece in self.pieces:
            for defender in temp.get_attacks(piece):
                attacks[str(len(attacks)) + ":" + str(self.move_value(piece, defender))] = [piece, defender]
        return attacks

    #removes any lost peices from corps
    def update_corp(self):
        temp = [x for x in self.pieces if self.board.get_piece(x) is not None]
        self.pieces = temp

    #calculates move value
    def move_value(self, attacker, defender):
        value = self.piece_value[self.board.get_piece(defender).unit] * \
                (1 - ((self.board.attack_values[
                           self.board.get_piece(attacker).unit + self.board.get_piece(defender).unit] - 1) / 6))
        return value
        # if self.board.get_piece(attacker).team == self.team:
        #     return self.offense * value
        # else:
        #     return -self.defense * value

    #this will be the function containing the move instructions
    def ai_move(self):
        rand = RandomAI(self.board, 1)
        targets = self.scan_for_targets()
        for corp in self.corps:
            targets.update(self.corps[corp].scan_for_targets())
        temp = None
        for i in targets:
            if temp is None:
                temp = i
            elif float(temp.split(":")[1]) < float(i.split(":")[1]):
                temp = i
        if temp is not None:
            print(self.board.attack(targets[temp][0], targets[temp][1]))
        print(rand.ai_rand_move())
        self.board.end_turn()
