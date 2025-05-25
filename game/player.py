
### File: player.py
from common.constants import PLAYER

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.symbol = PLAYER
        self.score = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy