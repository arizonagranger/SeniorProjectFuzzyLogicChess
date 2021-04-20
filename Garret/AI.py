from Board import Board
import random
from RandomAI import RandomAI


class AI:

    def __init__(self, board, team, corp="K"):
        self.location_value = {
            "k": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "q": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "p": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "n": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 3, 3, 3, 3, 3, 3, 0],
                [0, 3, 5, 5, 5, 5, 3, 0],
                [0, 3, 5, 10, 10, 5, 3, 0],
                [0, 3, 5, 10, 10, 5, 3, 0],
                [0, 3, 5, 5, 5, 5, 3, 0],
                [0, 3, 3, 3, 3, 3, 3, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "a": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 3, 3, 3, 3, 3, 3, 0],
                [0, 3, 5, 5, 5, 5, 3, 0],
                [0, 3, 5, 10, 10, 5, 3, 0],
                [0, 3, 5, 10, 10, 5, 3, 0],
                [0, 3, 5, 5, 5, 5, 3, 0],
                [0, 3, 3, 3, 3, 3, 3, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "i": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ],
        }
        self.piece_value = {"k": 700, "p": 500, "q": 500, "a": 500, "n": 500, "i": 500}
        self.offense = random.uniform(0.5, 1.5)
        self.defense = 1 - self.offense
        self.team = team
        self.board = board
        self.board_strings = [board.get_board()]
        self.corp = corp
        self.counter = 0
        self.previous = []
        if corp == "K":
            self.corps = {"L": AI(board, team, "L"), "R": AI(board, team, "R"), "K": self}
        self.pieces = self.board.get_del(self.team, self.corp)

    # check how many pieces are left in the corp
    def check_status(self, corp):
        self.update_corp()
        return len(self.corps[corp].pieces)

    def check_strength(self, corp):
        corp.update_corp()
        weak = True
        print(corp.pieces)
        for piece in corp.pieces:
            if self.board.get_piece(piece).unit not in ["p", "i"]:
                weak = False
        return weak

    def check_king_corp(self):
        self.update_corp()
        strong = []
        for piece in self.pieces:
            if self.board.get_piece(piece).unit not in ["k", "i"]:
                strong.append(piece)
        return strong

    # alters the offense or defense based on the amount of pieces
    def change_aggression(self):
        for corp in self.corps:
            if self.check_status(corp) / len(self.board.get_team(self.team)) > 0.3:
                self.corps[corp].offense += 0.5
            elif self.check_status(corp) / len(self.board.get_team(self.team)) < 0.15 and len(
                    self.check_status(self.corp)) > 3:
                self.corps[corp].defense += 0.5
            if self.check_strength(self.corps[corp]):
                kings_pieces = self.check_king_corp()
                if len(kings_pieces) > 1:
                    random.shuffle(kings_pieces)
                    self.board.del_piece(kings_pieces[0], corp)





    # finds the king and returns true if its in danger
    def king_threat(self):
        for x in self.pieces:
            if self.board.get_piece(x).unit == "k":
                return self.scan_threats_for(x.coord)
        return False

    # checks if there are any threats on the given location
    def scan_threats_for(self, coord):
        if coord in self.board.get_attacks(coord):
            return True
        else:
            False

    # finds threat level
    def scan_threat_level(self, board, piece):
        temp = Board(board.get_board())
        pieces = []
        attackers = []
        probability = 0
        for attacker in temp.get_team(abs(self.team - 1)):
            if piece in temp.get_attacks(attacker):
                attackers.append(attacker)
        while len(attackers) > 0:
            highest = attackers[0]
            for attacker in attackers:
                if temp.prob(attacker, piece) > temp.prob(highest, piece):
                    highest = attacker
            filtered = filter(lambda j: temp.get_piece(j).unit != temp.get_piece(highest).unit, attackers)
            attackers = list(filtered)
            pieces.append(highest)
        if len(pieces) != 0:
            probability = temp.prob(pieces.pop(0), piece)
            for x in pieces:
                probability += (1-probability) * temp.prob(x, piece)
            if self.board.get_piece(piece).unit == "K":
                return temp.get_piece(piece).value * 10 * probability
            return temp.get_piece(piece).value * probability
        else:
            return probability

    # returns a dictionary of value of the threat and the the pieces involved
    # higher defensive trait the higher this value should be
    def scan_threats(self):
        self.update_corp()
        temp = Board(self.board.get_board())
        temp.end_turn()
        for piece in temp.get_team(abs(1 - self.team)):
            self.board.get_piece(piece).threatValue = 0
            for attacks in temp.get_attacks(piece):
                if attacks in temp.get_team(self.team):
                    if self.board.get_piece(piece).threatValue < self.board.get_piece(
                            piece).value + self.board.get_piece(attacks).value * self.defense:
                        self.board.get_piece(piece).threatValue = self.board.get_piece(
                            piece).value + self.board.get_piece(attacks).value * self.defense

    # checks all possible attacks
    def scan_for_targets(self):
        self.update_corp()
        temp = Board(self.board.get_board())
        attacks = {}
        for piece in self.pieces:
            for defender in temp.get_attacks(piece):
                attacks[str(len(attacks)) + ":" + str(self.move_value(piece, defender))] = [piece, defender]
        return attacks

    # removes any lost peices from corps
    def update_corp(self):
        self.pieces = self.board.get_del(self.team, self.corp)
        empties = []
        if self.corp == "K":
            for corp in self.corps:
                if len(self.board.get_del(self.team, corp)) == 0:
                    empties.append(corp)
            for corp in empties:
                self.corps.pop(corp)
        for piece in self.board.get_team(self.team):
            self.board.get_piece(piece).threatLevel = self.scan_threat_level(self.board, piece)

    # calculates move value
    # higher offensive
    def move_value(self, board, attacker, defender):
        if board.get_piece(attacker).unit == "n" and not board.get_piece(attacker).move:
            prob = ((6 - board.attack_values[board.get_piece(attacker).unit + board.get_piece(defender).unit]) / 6)
        else:
            prob = ((7 - board.attack_values[board.get_piece(attacker).unit + board.get_piece(defender).unit]) / 6)
        if board.get_piece(defender).threatValue == 0:
            value = board.get_piece(defender).value * prob
        else:
            value = board.get_piece(defender).threatValue * prob * self.offense
        return value

    def threat_level_delta(self, board, piece):
        return (board.get_piece(piece).threatLevel - self.scan_threat_level(board, piece)) * self.defense

    def test_move_infa(self):
        rand_corps = ["L", "R"]
        random.shuffle(rand_corps)
        for i in rand_corps:
            self.corps[i].move_infa()

    def move_infa(self):
        self.update_corp()
        infantry = []
        for i in self.pieces:
            if self.board.get_piece(i) is not None and self.board.get_piece(i).unit == "i":
                infantry.append(i)
        random.shuffle(infantry)
        piece = infantry[0]
        moves = self.board.get_moves(piece)
        if len(moves) != 0:
            random.shuffle(moves)
            move = moves[0]
            self.board.move(piece, move)

    # **********************NOTE****************************
    # scan threats set value then run future moves
    # use future moves in scan

    def test_future_move(self):
        self.update_corp()
        self.change_aggression()
        self.counter += 1
        corps = list(self.corps.keys())
        if self.counter == 1:
            self.test_move_infa()
            corps.remove("R")
            corps.remove("L")
        print(self.counter)
        while len(corps) != 0:
            best = [[], [-88888, [0, [0, 0]]]]
            for corp in corps:
                move = self.corps[corp].get_future_moves()
                if move[1][0] > best[1][0]:
                    best = move
            corps.remove(self.board.get_piece(best[0]).delegation)
            if move[1][1][0] == 1:
                print("attack ", self.board.get_piece(best[0]).delegation, " : ", best[0], best[1][1][1], ":",
                      self.board.attack(best[0], best[1][1][1]))
            else:
                print("move ", self.board.get_piece(best[0]).delegation, " : ", best[0], ":", best[1][1][1])
                self.board.move(best[0], best[1][1][1])
        self.board.update_pieces()
        for piece in self.board.get_team(self.team):
            print(piece,":", self.board.get_piece(piece).move," and ", self.board.get_piece(piece).attack)
        for piece in self.board.get_team(self.team):
            if len(self.board.get_attacks(piece)) != 0:
                print("attack from: ", piece)
                self.board.attack(piece, self.board.get_attacks(piece)[0])


    def get_future_moves(self):
        self.update_corp()
        self.scan_threats()
        best = [[], [-99999, [0, [0, 0]]]]
        for piece in self.pieces:
            self.previous = []
            move = self.future_move(piece, self.board, piece, 0)
            if move[0] > best[1][0]:
                best = [piece, move]
        return best

    def future_move(self, piece, board, move, turns, previous=[]):
        temp = Board("W64")
        temp.copy_board(board)
        temp.update_pieces()
        if turns != 0:
            temp.set_piece(piece, move)
            self.previous += previous
            self.previous = [list(t) for t in set(tuple(element) for element in self.previous)]
            piece = move
        attacks_values = []
        best = [-1111111, [0, [0, 0]]]
        for attacks in temp.get_attacks(piece):
            if temp.get_piece(piece).unit == "n":
                attacks_values.append([self.move_value(temp, piece, attacks) + self.test_move(temp, piece, attacks) - ((turns-1) * 100), [1, attacks]])
            else:
                attacks_values.append(
                    [self.move_value(temp, piece, attacks) + self.test_move(temp, piece, attacks) - (turns * 100),
                     [1, attacks]])
        if turns < 5 and temp.get_piece(piece).unit != "n" and temp.get_piece(piece).unit != "q" and temp.get_piece(
                piece).unit != "k":
            moves = temp.get_moves(piece)
            for move in moves:
                attacks_values.append([self.future_move(piece, temp, move, turns + 1) + self.test_move(temp, piece, move), [0, move]])
        elif turns < 2 and (temp.get_piece(piece).unit == "q" or temp.get_piece(piece).unit == "k"):
            moves = temp.get_moves(piece)
            for move in moves:
                attacks_values.append([self.future_move(piece, temp, move, turns + 1, moves) + self.test_move(temp, piece, move), [0, move]])
        elif turns < 1 and (temp.get_piece(piece).unit == "n"):
            moves = temp.get_moves(piece)
            for move in moves:
                attacks_values.append([self.future_move(piece, temp, move, turns + 1, moves) + self.test_move(temp, piece, move), [0, move]])
        for attack in attacks_values:
            if attack[0] > best[0]:
                best = attack
        if turns == 0:
            return best
        return best[0]

    def test_move(self, board, piece, move):
        temp = Board(board.get_board())
        temp.end_turn()
        temp.set_piece(piece, move)
        return self.threat_level_delta(temp, move)

    def testing_stuff(self):
        for piece in self.board.get_team(self.team):
            print(self.future_move(piece, self.board, piece, 0))
