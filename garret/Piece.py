class Piece:
    def __init__(self, team, unit, delegation, coord):
        speeds = {"i": 1, "a": 1, "n": 5, "p": 1, "q": 3, "k": 3}
        self.speed = speeds[unit]
        self.team = team
        self.unit = unit
        self.delegation = delegation
        self.coord = coord
        self.attack = True
        self.move = True
