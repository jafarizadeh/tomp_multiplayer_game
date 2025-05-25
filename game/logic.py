
### File: logic.py
from common.constants import *
import random

def handle_move(game_map, player, dx, dy):
    nx, ny = player.x + dx, player.y + dy

    if not (0 <= nx < game_map.width and 0 <= ny < game_map.height):
        return

    cell = game_map.get_cell(nx, ny)

    if cell == WALL:
        return
    elif cell == STAR:
        player.score += 1
        game_map.set_cell(nx, ny, EMPTY)
    elif cell == TRAPPED_STAR:
        game_map.set_cell(nx, ny, STAR)
    elif cell == TRAP:
        infect_stars(game_map)
    elif cell == ENEMY:
        add_stars(game_map)
    elif cell == LAVA:
        game_map.reset_stars()

    player.move(dx, dy)

def infect_stars(game_map, count=3):
    # Randomly turn some stars into trapped stars
    stars = [(x, y) for y in range(game_map.height) for x in range(game_map.width) if game_map.get_cell(x, y) == STAR]
    for x, y in random.sample(stars, min(count, len(stars))):
        game_map.set_cell(x, y, TRAPPED_STAR)

def add_stars(game_map, count=5):
    # Randomly add new stars to empty locations
    empties = [(x, y) for y in range(game_map.height) for x in range(game_map.width) if game_map.get_cell(x, y) == EMPTY]
    for x, y in random.sample(empties, min(count, len(empties))):
        game_map.set_cell(x, y, STAR)

