class Piece:
    def __init__(self, team, unit, delegation, coord):
        speeds = {"i": 1, "a": 1, "n": 5, "p": 1, "q": 3, "k": 3}
        values = {"k": 2000, "p": 500, "q": 300, "a": 400, "n": 400, "i": 50}
        self.value = values[unit]
        self.threatValue = values[unit]
        self.threatLevel = 0
        self.speed = speeds[unit]
        self.team = team
        self.unit = unit
        self.delegation = delegation
        self.coord = coord
        self.attack = True
        self.move = True
