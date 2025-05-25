# Directions
UP = "w"
DOWN = "s"
LEFT = "a"
RIGHT = "d"

VALID_DIRECTIONS = {
    UP: (-1, 0),     # row - 1
    DOWN: (1, 0),    # row + 1
    LEFT: (0, -1),   # col - 1
    RIGHT: (0, 1),   # col + 1
}

# Tile definitions
TILE_EMPTY = "."
TILE_WALL = "#"
TILE_STAR = "*"
TILE_STAR_CORRUPT = "@"
TILE_TRAP = "^"
TILE_LAVA = "~"
TILE_ENEMY = "&"

SPECIAL_TILES = {
    TILE_STAR,
    TILE_STAR_CORRUPT,
    TILE_TRAP,
    TILE_LAVA,
    TILE_ENEMY
}

# Game rule values
STAR_REQUIRED_RATIO = 0.8   # 80% of stars required to win
STARS_LOST_ON_ENEMY = 5

# Characters used for players (A-Z)
PLAYER_SYMBOLS = [chr(c) for c in range(ord("A"), ord("Z")+1)]
