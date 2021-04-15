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

    # returns a dictionary of value of the threat and the the pieces involved
    # higher defensive trait the higher this value should be
    def scan_threats(self):
        self.update_corp()
        temp = Board(self.board.get_board())
        temp.end_turn()
        for piece in temp.get_team(abs(1 - self.team)):
            self.board.get_piece(piece).threatValue = [0, 0]
            for attacks in temp.get_attacks(piece):
                if attacks in self.pieces:
                    if self.board.get_piece(piece).threatValue[self.team] < self.board.get_piece(
                            piece).value + self.board.get_piece(attacks).value * 100 * self.defense:
                        self.board.get_piece(piece).threatValue[self.team] = self.board.get_piece(
                            piece).value + self.board.get_piece(attacks).value * 100 * self.defense

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

    # calculates move value
    # higher offensive
    def move_value(self, board, attacker, defender):
        if board.get_piece(attacker).unit == "n" and not board.get_piece(attacker).move:
            prob = ((6 - board.attack_values[board.get_piece(attacker).unit + board.get_piece(defender).unit]) / 6)
        else:
            prob = ((7 - board.attack_values[board.get_piece(attacker).unit + board.get_piece(defender).unit]) / 6)
        if board.get_piece(defender).threatValue[self.team] == 0:
            value = board.get_piece(defender).value * prob
        else:
            value = board.get_piece(defender).threatValue[self.team] * prob * self.offense
        return value

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
    # scan threats set value then run futur moves
    # use futur moves in scan
    
    #runs through each corp and implements the best move
    def test_future_move(self):
        self.update_corp()
        if self.board.get_board()[:33] == "BAKNRPRQKKKPLNLAKIRIRIRIKIKILILIL":
            self.test_move_infa()
        corps = list(self.corps.keys())
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
                
    #runs future moves for each piece and finds the piece with best possible move
    def get_future_moves(self):
        self.update_corp()
        self.scan_threats()
        best = [[], [-99999, [0, [0, 0]]]]
        for piece in self.pieces:
            move = self.future_move(piece, self.board, piece, 0)
            if move[0] > best[1][0]:
                best = [piece, move]
        return best
    
    # recursivley called function that creates a new board and runs through available moves
    def future_move(self, piece, board, move, turns):
        temp = Board("W64")
        temp.copy_board(board)
        temp.update_pieces()
        if turns != 0:
            temp.set_piece(piece, move)
        piece = move
        moves = temp.get_moves(piece)
        attacks_values = []
        best = [-1111111, [0, [0, 0]]]
        for attacks in temp.get_attacks(piece):
            attacks_values.append([self.move_value(temp, piece, attacks) - (turns * 100), [1, attacks]])
        if turns < 5 and temp.get_piece(piece).unit != "n" and temp.get_piece(piece).unit != "q" and temp.get_piece(
                piece).unit != "k":
            for move in moves:
                attacks_values.append([self.future_move(piece, temp, move, turns + 1), [0, move]])
        elif turns < 1 and (temp.get_piece(piece).unit == "n" or temp.get_piece(piece).unit == "q" or temp.get_piece(
                piece).unit == "k"):
            for move in moves:
                attacks_values.append([self.future_move(piece, temp, move, turns + 1), [0, move]])
        for attack in attacks_values:
            if attack[0] > best[0]:
                best = attack
        if turns == 0:
            return best
        return best[0]
