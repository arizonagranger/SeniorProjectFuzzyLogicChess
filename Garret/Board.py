from Piece import Piece
import random


class Board:

    def __init__(self, boardString):
        self.board = []
        self.captured = []
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

    #sets all the pieces on the team that cant move
    def set_turn(self, team):
        for x in self.board:
            for y in x:
                if y is not None and y.team != team:
                    y.attack = False
                    y.move = False

    #returns the board string
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
    
    #returns all coordinates of a delegation in a list
    def get_del(self, team, delegation):
        self.update_pieces()
        del_list = []
        for x in self.board:
            for y in x:
                if y is not None and y.delegation == delegation and y.team == team:
                    del_list.append(y.coord)
        return del_list
    
    #returns a list of the coordinates of all pieces
    def get_team(self, team):
        del_list = []
        for x in self.board:
            for y in x:
                if y is not None and y.team == team:
                    del_list.append(y.coord)
        return del_list
    
    #returns a list of all possible locations to move for the piece
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
    
    #called by get move and is recursivley called to find the reach of a piece
    def get_moves_speed(self, coord, speed):
        moves = []
        if coord[0] >= 8 or coord[0] < 0 or coord[1] >= 8 or coord[1] < 0 or self.board[coord[0]][coord[1]] != None:
            return [0]
        elif speed == 0:
            return [coord]
        else:
            moves += [coord]
            for x in [0, -1, 1]:
                for y in [-1, 1]:
                    moves += (self.get_moves_speed([coord[0] + x, coord[1] + y], speed - 1))
                    moves += (self.get_moves_speed([coord[0] + y, coord[1] + x], speed - 1))
        return moves

    #returns a list of the possible places to attck for a piece
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
                for x in range(4):
                    for y in range(4):
                        for j in [1,-1]:
                            for i in [1,-1]:
                                try:
                                    if self.board[coord[0] + (j * x)][coord[1] + (i * y)].team == abs(team - 1):
                                        attacks.append([coord[0] + (j * x), coord[1] + (i * y)])
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

    #activates a move returns true if the move happened
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
    
    #sets all the pieces coordinates to where they are on the field
    def update_pieces(self):
        for x in range(len(self.board)):
            for y in range(len(self.board)):
                if self.board[x][y] is not None:
                    self.board[x][y].coord = [x, y]

    #returns true or false if the coord is in the range of the attacking unit at the attacking location
    def in_range(self, unit, attacker, coord):
        for x in [0, -1, 1]:
            for y in [-1, 1]:
                try:
                    if [attacker[0] + x, attacker[1] + y] == coord:
                        return True
                except:
                    pass
                try:
                    if [attacker[0] + y, attacker[1] + x] == coord:
                        return True
                except:
                    pass
        if unit == "a":
            for x in range(4):
                for y in range(4):
                    for j in [1, -1]:
                        for i in [1, -1]:
                            try:
                                if self.board[coord[0] + (j * x)][coord[1] + (i * y)].team == coord:
                                    return True
                            except:
                                pass
        return False

    #sets the attack and returns the outcome and role in a list 0 if failed and 1 if succsess
    #[1 or 0, 1-6 (roll)]
    def attack(self, attacker, defender):
        self.update_pieces()
        if self.board[attacker[0]][attacker[1]] is not None and defender in self.get_attacks(attacker):
            self.update_pieces()
            roll = random.randrange(1, 7)
            self.board[attacker[0]][attacker[1]].move = False
            self.board[attacker[0]][attacker[1]].attack = False
            if self.board[attacker[0]][attacker[1]].unit == "n" and not self.board[attacker[0]][attacker[1]].move:
                roll -= 1
            if roll >= self.attack_values[
                str(self.board[attacker[0]][attacker[1]].unit) + str(self.board[defender[0]][defender[1]].unit)]:
                self.captured.append(self.board[defender[0]][defender[1]])
                for x in self.get_del(self.board[attacker[0]][attacker[1]].team,
                                      self.board[attacker[0]][attacker[1]].delegation):
                    self.board[x[0]][x[1]].move = False
                    self.board[x[0]][x[1]].attack = False
                if self.board[defender[0]][defender[1]].unit == "p":
                    self.corp_dead(self.board[defender[0]][defender[1]].team,
                                   self.board[defender[0]][defender[1]].delegation)
                    if self.board[attacker[0]][attacker[1]].unit == "a":
                        self.board[defender[0]][defender[1]] = None
                    else:
                        self.board[defender[0]][defender[1]] = self.board[attacker[0]][attacker[1]]
                        self.board[attacker[0]][attacker[1]] = None
                elif self.board[defender[0]][defender[1]].unit == "k":
                    self.king_dead(self.board[defender[0]][defender[1]].team)
                    if self.board[attacker[0]][attacker[1]].unit == "a":
                        self.board[defender[0]][defender[1]] = None
                    else:
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

    #activates if the corp leader is taken then sets all pieces in that corp to the kings corp
    def corp_dead(self, team, corps):
        for pieces in self.get_del(team, corps):
            self.board[pieces[0]][pieces[1]].delegation = "K"
    
    #sets piece to the given corp if its legal
    def del_piece(self, piece, corps):
        if self.board[piece[0]][piece[1]].delegation == "K" and self.board[piece[0]][piece[1]].unit != "k":
            self.board[piece[0]][piece[1]].delegation = corps

    #activates if king is dead
    def king_dead(self, team):
        self.state = abs(team - 1)

    #switches the board to the next teams turn 
    def end_turn(self):
        for x in self.board:
            for y in x:
                if y is not None:
                    y.attack = True
                    y.move = True
        self.turn = abs(self.turn - 1)
        self.set_turn(self.turn)

    #returns the piece at the given coord
    def get_piece(self, coord):
        return self.board[coord[0]][coord[1]]

    #adds a piece to the board
    def add_piece(self, team, unit, delegation, coord):
        self.board[coord[0]][coord[1]] = Piece(team, unit, delegation, coord)
        self.update_pieces()

    #removes piece from given coord
    def delete_piece(self, coord):
        self.board[coord[0]][coord[1]] = None
        self.update_pieces()

    #moves piece to the given coord
    def set_piece(self, piece, coord):
        self.board[coord[0]][coord[1]] = self.board[piece[0]][piece[1]]
        self.board[piece[0]][piece[1]] = None
        self.update_pieces()

    #prints a board
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

    #prints board showing possible moves
    def show_moves(self, coord):
        moves = self.get_moves(coord)
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
                    elif [x, y] in moves:
                        print(u"\u25A0", end=" ")
                    else:
                        print(0, end=" ")
                print()

    #prints board with higlighted enemies to attack
    def show_attacks(self, coord):
        attacks = self.get_attacks(coord)
        print(attacks)
        if self.board[coord[0]][coord[1]] is not None:
            for x in range(8):
                for y in range(8):
                    if self.board[x][y] is not None:
                        if [x, y] == coord:
                            print("\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(150,150,15, self.board[x][y].unit), end="")
                        elif self.board[x][y].team == 1:
                            if [x, y] in attacks:
                                print("\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(150, 80, 15,
                                                                                            self.board[x][y].unit),end="")
                            else:
                                print(self.board[x][y].unit.upper(), end=" ")
                        else:
                            print(self.board[x][y].unit, end=" ")
                    else:
                        print(0, end=" ")
                print()
     
     def prob(self, attacker, defender):
        value = self.attack_values.get([str(attacker.unit)+str(defender.unit)])
        prob = value/6
        return prob
