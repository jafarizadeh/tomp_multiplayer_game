# --------------------------
# FILE: game_map.py
# Purpose: Stores and manipulates 2D game map
# --------------------------

from common.constants import *
import random

class GameMap:
    def __init__(self, map_lines):
        """
        Initialize the game map from a list of strings.
        Each line is a row of the map.
        """
        self.grid = [list(row) for row in map_lines]
        self.height = len(self.grid)
        self.width = len(self.grid[0]) if self.grid else 0

    def in_bounds(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width

    def get_tile(self, x, y):
        if self.in_bounds(x, y):
            return self.grid[x][y]
        return TILE_WALL  # Treat out-of-bounds as wall

    def set_tile(self, x, y, value):
        if self.in_bounds(x, y):
            self.grid[x][y] = value

    def find_all(self, target_tile):
        """
        Return a list of all (x, y) coordinates containing the given tile.
        """
        positions = []
        for x in range(self.height):
            for y in range(self.width):
                if self.grid[x][y] == target_tile:
                    positions.append((x, y))
        return positions

    def find_empty(self):
        """
        Return a random empty (non-wall) location.
        """
        empty_tiles = []
        for x in range(self.height):
            for y in range(self.width):
                if self.grid[x][y] == TILE_EMPTY:
                    empty_tiles.append((x, y))
        return random.choice(empty_tiles) if empty_tiles else (1, 1)

    def as_string_list(self):
        return ["".join(row) for row in self.grid]

    def clone(self):
        return GameMap(self.as_string_list())

    def __repr__(self):
        return "\n".join(self.as_string_list())