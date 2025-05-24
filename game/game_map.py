class GameMap:
    def __init__(self, map_data):
        self.grid = [list(row) for row in map_data]
        self.original_star_positions = []

    def get_tile(self, x, y):
        return self.grid[y][x]

    def set_tile(self, x, y, tile):
        self.grid[y][x] = tile

    def find_all(self, tile):
        positions = []
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if char == tile:
                    positions.append((x, y))
        return positions
