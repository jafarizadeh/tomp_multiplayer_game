from common.constants import *

class GameMap:
    def __init__(self):
        self.raw_map = [
            "###############",
            "#....*....*...#",
            "#..^..#..&....#",
            "#....~.....^..#",
            "#.*....*......#",
            "###############"
        ]
        self.height = len(self.raw_map)
        self.width = len(self.raw_map[0])
        self.map = [[cell for cell in row] for row in self.raw_map]
        self.initial_stars = self.find_initial_stars()

    def find_initial_stars(self):
        stars = {}
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == STAR:
                    stars[(x, y)] = STAR
        return stars

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
        for (x, y), _ in self.initial_stars.items():
            self.map[y][x] = STAR

    def count_collected_stars(self):
        return sum(1 for (x, y) in self.initial_stars if self.map[y][x] == EMPTY)

    def total_initial_stars(self):
        return len(self.initial_stars)
