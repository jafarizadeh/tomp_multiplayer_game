from game.game_map import GameMap
from game.player import Player
from game.logic import handle_move
import os
import msvcrt  # برای دریافت مستقیم کلید

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def move_until_wall(game_map, player, dx, dy):
    while True:
        nx, ny = player.x + dx, player.y + dy
        if not (0 <= nx < game_map.width and 0 <= ny < game_map.height):
            break
        if game_map.get_cell(nx, ny) == '#':
            break
        handle_move(game_map, player, dx, dy)

def main():
    game_map = GameMap()
    player = Player(x=1, y=1)

    while True:
        clear()
        game_map.render(player)
        print(f"Score: {player.score}")
        print("Use keys: A (←), D (→), W (↑), S (↓) — Press key to move")

        if game_map.count_collected_stars() >= 0.8 * game_map.total_initial_stars():
            print("🎉 Level Completed!")
            break

        key = msvcrt.getch().decode('utf-8').lower()

        if key == 'a':
            move_until_wall(game_map, player, -1, 0)
        elif key == 'd':
            move_until_wall(game_map, player, 1, 0)
        elif key == 'w':
            move_until_wall(game_map, player, 0, -1)
        elif key == 's':
            move_until_wall(game_map, player, 0, 1)

if __name__ == '__main__':
    main()
