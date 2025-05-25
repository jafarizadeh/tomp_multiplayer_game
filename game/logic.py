from common.constants import *
import random

def handle_move(game_map, player, dx, dy):
    nx, ny = player.x + dx, player.y + dy

    # Check if the destination is inside the map
    if not (0 <= nx < game_map.width and 0 <= ny < game_map.height):
        return

    cell = game_map.get_cell(nx, ny)

    if cell == WALL:
        return  # Cannot move into a wall

    # Save current position
    prev_x, prev_y = player.x, player.y
    moved = False

    # Logic based on cell content
    if cell == STAR:
        player.score += 1
        game_map.set_cell(nx, ny, EMPTY)
        moved = True

    elif cell == TRAPPED_STAR:
        # First pass: turn @ into *
        game_map.set_cell(nx, ny, STAR)
        return  # Stay in place, don't move yet

    elif cell == TRAP:
        infect_stars(game_map)
        moved = True

    elif cell == ENEMY:
        add_stars(game_map)
        moved = True

    elif cell == LAVA:
        game_map.reset_stars()
        moved = True

    elif cell == EMPTY:
        moved = True

    if moved:
        # Clear previous position and move player
        game_map.set_cell(prev_x, prev_y, EMPTY)
        player.move(dx, dy)

def infect_stars(game_map, count=3):
    """Convert some stars (*) into trapped stars (@)."""
    stars = [
        (x, y)
        for y in range(game_map.height)
        for x in range(game_map.width)
        if game_map.get_cell(x, y) == STAR
    ]
    for x, y in random.sample(stars, min(count, len(stars))):
        game_map.set_cell(x, y, TRAPPED_STAR)

def add_stars(game_map, count=5):
    """Add new stars (*) to empty locations (.)."""
    empties = [
        (x, y)
        for y in range(game_map.height)
        for x in range(game_map.width)
        if game_map.get_cell(x, y) == EMPTY
    ]
    for x, y in random.sample(empties, min(count, len(empties))):
        game_map.set_cell(x, y, STAR)
