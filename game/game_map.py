
### File: game_map.py
import random
from common.constants import *

class GameMap:
    def __init__(self, width, height, star_count):
        self.width = width
        self.height = height
        self.map = [[EMPTY for _ in range(width)] for _ in range(height)]
        self.initial_stars = {}
        self.place_random_elements(star_count)

    def place_random_elements(self, star_count):
        # Randomly place stars and some special elements
        positions = random.sample([(x, y) for x in range(self.width) for y in range(self.height)], star_count + 5)
        for i in range(star_count):
            x, y = positions[i]
            self.map[y][x] = STAR
            self.initial_stars[(x, y)] = STAR
        for x, y in positions[star_count:]:
            self.map[y][x] = random.choice([TRAP, ENEMY, LAVA])

    def render(self, player):
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                if (x, y) == (player.x, player.y):
                    row += player.symbol
                else:
                    row += self.map[y][x]
            print(row)

    def get_cell(self, x, y):
        return self.map[y][x]

    def set_cell(self, x, y, value):
        self.map[y][x] = value

    def reset_stars(self):
        # Reset all stars to initial positions
        for (x, y), _ in self.initial_stars.items():
            self.map[y][x] = STAR

    def count_collected_stars(self):
        # Count how many stars have been collected
        return sum(1 for (x, y) in self.initial_stars if self.map[y][x] == EMPTY)

    def total_initial_stars(self):
        return len(self.initial_stars)