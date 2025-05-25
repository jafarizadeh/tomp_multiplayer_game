from common.constants import *

class GameMap:
    def __init__(self, map_data):
        """
        Initialize the game map from a list of strings.
        Each row is converted to a list of characters.
        """
        self.grid = [list(row) for row in map_data]
        self.original_star_positions = self.find_all(TILE_STAR)

    def get_tile(self, x, y):
        """
        Return the tile at position (x, y).
        """
        return self.grid[y][x]

    def set_tile(self, x, y, value):
        """
        Set the tile at position (x, y) to the given value.
        """
        self.grid[y][x] = value

    def find_all(self, tile_type):
        """
        Return a list of all (x, y) positions that contain the given tile type.
        """
        positions = []
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile == tile_type:
                    positions.append((x, y))
        return positions

    def is_within_bounds(self, x, y):
        """
        Check if the (x, y) coordinate is within the map boundaries.
        """
        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0])

    def as_string_list(self):
        """
        Return the map as a list of strings, suitable for sending to clients.
        """
        return ["".join(row) for row in self.grid]

    def clone(self):
        """
        Return a deep copy of the current map grid.
        """
        return [row[:] for row in self.grid]
