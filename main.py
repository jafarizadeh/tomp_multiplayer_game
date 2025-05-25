
### File: main.py
from game.game_map import GameMap
from game.player import Player
from game.logic import handle_move

import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    width, height = 10, 10
    game_map = GameMap(width, height, star_count=10)
    player = Player(x=0, y=0)

    while True:
        clear()
        game_map.render(player)
        print(f"Score: {player.score}")

        if game_map.count_collected_stars() >= 0.8 * game_map.total_initial_stars():
            print("🎉 Level Completed!")
            break

        move = input("Move (WASD): ").lower()
        dx, dy = 0, 0
        if move == 'w': dy = -1
        elif move == 's': dy = 1
        elif move == 'a': dx = -1
        elif move == 'd': dx = 1

        handle_move(game_map, player, dx, dy)

if __name__ == '__main__':
    main()
