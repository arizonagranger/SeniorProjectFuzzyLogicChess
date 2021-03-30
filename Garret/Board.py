from Piece import Piece
import random


class Board:

    def __init__(self, boardString):
        self.board = []
        self.state = 2
        self.attack_values = {
            "kk": 4, "kq": 4, "kn": 4, "kp": 4, "ka": 5, "ki": 1,
            "qk": 4, "qq": 4, "qn": 4, "qp": 4, "qa": 5, "qi": 2,
            "nk": 6, "nq": 6, "nn": 4, "np": 4, "na": 5, "ni": 2,
            "pk": 5, "pq": 5, "pn": 5, "pp": 4, "pa": 5, "pi": 3,
            "ak": 4, "aq": 4, "an": 5, "ap": 5, "aa": 6, "ai": 5,
            "ik": 6, "iq": 6, "in": 6, "ip": 5, "ia": 6, "ii": 4,
        }
        for x in range(8):
            self.board.append([])
            for y in range(8):
                self.board[x].append(None)

        types = {
            "i": 1, "a": 2, "n": 3, "p": 4, "q": 5, "k": 6
        }

        delegations = {
            "L": 2, "K": 3, "R": 1
        }

        if boardString[:1] == "W":
            self.turn = 0
        else:
            self.turn = 1
        boardString = boardString[1:]

        x = 0
        while len(boardString) > 0:
            if not boardString[0].isnumeric():
                piece = boardString[:2]
                boardString = boardString[2:]
                if piece[0].isupper():
                    self.board[int(x / 8)][x % 8] = Piece(1, piece[0].lower(), piece[1], [int(x / 8), x % 8])
                else:
                    self.board[int(x / 8)][x % 8] = Piece(0, piece[0].lower(), piece[1], [int(x / 8), x % 8])
                x += 1
            else:
                if len(boardString) > 1 and boardString[1].isnumeric():
                    number = boardString[:2]
                    boardString = boardString[2:]
                else:
                    number = boardString[:1]
                    boardString = boardString[1:]
                for y in range(int(number)):
                    self.board[int(x / 8)][x % 8] = None
                    x += 1
        self.set_turn(self.turn)

    def set_turn(self, team):
        for x in self.board:
            for y in x:
                if y is not None and y.team != team:
                    y.attack = False
                    y.move = False

    def get_board(self):
        if self.turn == 0:
            boardString = "W"
        else:
            boardString = "B"
        number = 0
        for x in self.board:
            for y in x:
                if y is not None:
                    if number > 0:
                        boardString += str(number)
                        number = 0
                    if y.team == 1:
                        boardString += (y.unit.upper() + y.delegation)
                    else:
                        boardString += (y.unit + y.delegation)
                else:
                    number += 1
        return boardString

    def get_del(self, team, delegation):
        self.update_pieces()
        del_list = []
        for x in self.board:
            for y in x:
                if y is not None and y.delegation == delegation and y.team == team:
                    del_list.append(y.coord)
        return del_list

    def get_team(self, team):
        del_list = []
        for x in self.board:
            for y in x:
                if y is not None and y.team == team:
                    del_list.append(y.coord)
        return del_list

    def get_moves(self, coord):
        self.update_pieces()
        if self.board[coord[0]][coord[1]].move:
            team = self.board[coord[0]][coord[1]].team
            unit = self.board[coord[0]][coord[1]].unit
            speed = self.board[coord[0]][coord[1]].speed
            moves = [0]
            for x in [0, -1, 1]:
                for y in [-1, 1]:
                    moves += (self.get_moves_speed([coord[0] + x, coord[1] + y], speed - 1))
                    moves += (self.get_moves_speed([coord[0] + y, coord[1] + x], speed - 1))
            res = []
            [res.append(x) for x in moves if x not in res]
            res.pop(0)
            if unit == "i" or unit == "p":
                if team == 1:
                    moves = [x for x in res if x[0] > coord[0]]
                else:
                    moves = [x for x in res if x[0] < coord[0]]
                return moves
            return res
        else:
            return []

    def get_moves_speed(self, coord, speed):
        moves = []
        if coord[0] >= 8 or coord[0] < 0 or coord[1] >= 8 or coord[1] < 0 or self.board[coord[0]][coord[1]] != None:
            return [0]
        elif speed == 0:
            return [coord]
        else:
            for x in [0, -1, 1]:
                for y in [-1, 1]:
                    moves += (self.get_moves_speed([coord[0] + x, coord[1] + y], speed - 1))
                    moves += (self.get_moves_speed([coord[0] + y, coord[1] + x], speed - 1))
        return moves

    def get_attacks(self, coord):
        self.update_pieces()
        if self.board[coord[0]][coord[1]].attack:
            unit = self.board[coord[0]][coord[1]].unit
            team = self.board[coord[0]][coord[1]].team
            attacks = []
            for x in [0, -1, 1]:
                for y in [-1, 1]:
                    try:
                        if self.board[coord[0] + x][coord[1] + y].team == abs(team - 1):
                            attacks.append([coord[0] + x, coord[1] + y])
                    except:
                        pass
                    try:
                        if self.board[coord[0] + y][coord[1] + x].team == abs(team - 1):
                            attacks.append([coord[0] + y, coord[1] + x])
                    except:
                        pass
            if unit == "a":
                for i in [2, 3]:
                    for x in [0, -i, i]:
                        for y in [-i, i]:
                            try:
                                if self.board[coord[0] + x][coord[1] + y].team == abs(team - 1):
                                    attacks.append([coord[0] + x, coord[1] + y])
                            except:
                                pass
                            try:
                                if self.board[coord[0] + y][coord[1] + x].team == abs(team - 1):
                                    attacks.append([coord[0] + y, coord[1] + x])
                            except:
                                pass
            res = []
            [res.append(x) for x in attacks if x not in res]
            if unit == "i" or unit == "p":
                if team == 1:
                    moves = [x for x in res if x[0] > coord[0]]
                else:
                    moves = [x for x in res if x[0] < coord[0]]
            moves = res
            testx = [x for x in moves if x[0] <= 7 and x[0] >= 0]
            testy = [x for x in testx if x[1] <= 7 and x[1] >= 0]
            return testy
        else:
            return []

    def move(self, piece, coord):
        self.update_pieces()
        if self.board[piece[0]][piece[1]] is not None and coord in self.get_moves(piece) and self.board[piece[0]][
            piece[1]].move:
            for x in self.get_del(self.board[piece[0]][piece[1]].team, self.board[piece[0]][piece[1]].delegation):
                self.board[x[0]][x[1]].move = False
                self.board[x[0]][x[1]].attack = False
            if self.board[piece[0]][piece[1]].unit == "n":
                self.board[piece[0]][piece[1]].attack = True
            self.board[coord[0]][coord[1]] = self.board[piece[0]][piece[1]]
            self.board[piece[0]][piece[1]] = None
            self.board[coord[0]][coord[1]].move = False
            return True
        else:
            return False

    def update_pieces(self):
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] is not None:
                    self.board[x][y].coord = [x, y]

    def can_attack(self, attacker, coord):
      print("can attack")

    def attack(self, attacker, defender):
        self.update_pieces()
        if self.board[attacker[0]][attacker[1]] is not None and defender in self.get_attacks(attacker):
            self.update_pieces()
            roll = random.randrange(1, 7)
            if self.board[attacker[0]][attacker[1]].unit == "n" and not self.board[attacker[0]][attacker[1]].move:
                roll -= 1
            if roll >= self.attack_values[
                str(self.board[attacker[0]][attacker[1]].unit) + str(self.board[defender[0]][defender[1]].unit)]:
                for x in self.get_del(self.board[attacker[0]][attacker[1]].team,
                                      self.board[attacker[0]][attacker[1]].delegation):
                    self.board[x[0]][x[1]].move = False
                    self.board[x[0]][x[1]].attack = False
                if self.board[defender[0]][defender[1]].unit == "p":
                    self.corp_dead(self.board[defender[0]][defender[1]].team,
                                   self.board[defender[0]][defender[1]].delegation)
                elif self.board[defender[0]][defender[1]].unit == "k":
                    self.king_dead(self.board[defender[0]][defender[1]].team)
                    self.board[defender[0]][defender[1]] = self.board[attacker[0]][attacker[1]]
                    self.board[attacker[0]][attacker[1]] = None
                    return [2, roll]
                elif self.board[attacker[0]][attacker[1]].unit == "a":
                    self.board[defender[0]][defender[1]] = None
                else:
                    self.board[defender[0]][defender[1]] = self.board[attacker[0]][attacker[1]]
                    self.board[attacker[0]][attacker[1]] = None
                return [1, roll]
            else:
                return [0, roll]
        else:
            return [0, 0]

    def corp_dead(self, team, corps):
        for pieces in self.get_del(team, corps):
            self.board[pieces[0]][pieces[1]].delegation = "K"

    def del_piece(self, piece, corps):
        if self.board[piece[0]][piece[1]].delegation == "K" and self.board[piece[0]][piece[1]].unit != "k":
            self.board[piece[0]][piece[1]].delegation = corps

    def king_dead(self, team):
        self.state = abs(team - 1)

    def end_turn(self):
        for x in self.board:
            for y in x:
                if y is not None:
                    y.attack = True
                    y.move = True
        self.turn = abs(self.turn - 1)
        self.set_turn(self.turn)

    def get_piece(self, coord):
        return self.board[coord[0]][coord[1]]

    def add_piece(self, team, unit, delegation, coord):
        self.board[coord[0]][coord[1]] = Piece(team, unit, delegation, coord)

    def show_board(self):
        for x in range(len(self.board)):
            print()
            for y in range(len(self.board)):
                if self.board[x][y] != None:
                    if self.board[x][y].team == 1:
                        print(self.board[x][y].unit.upper(), end=" ")
                    else:
                        print(self.board[x][y].unit, end=" ")
                else:
                    print("0", end=" ")
        print("\n")

    def show_moves(self, coord):
        if self.board[coord[0]][coord[1]] is not None:
            for x in range(8):
                for y in range(8):
                    if self.board[x][y] is not None:
                        if [x, y] == coord:
                            print("\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(150,150,15, self.board[x][y].unit), end="")
                        elif self.board[x][y].team == 1:
                            print(self.board[x][y].unit.upper(), end=" ")
                        else:
                            print(self.board[x][y].unit, end=" ")
                    elif [x, y] in self.get_moves(coord):
                        print(u"\u25A0", end=" ")
                    else:
                        print(0, end=" ")
                print()
