from game.player import Player
from common.constants import *
from utils.rand import SimpleRandom

rand = SimpleRandom()

class GameLogic:
    def __init__(self, game_map):
        self.game_map = game_map                     # Avoid using 'map' (reserved)
        self.players = {}                            # player_id → Player
        self.events = []                             # List of recent game events

    def add_player(self, player):
        self.players[player.id] = player

    def handle_move(self, player_id, direction):
        """
        Move the player in the given direction until hitting a wall.
        At each step, handle any tile-specific logic (star, trap, etc.).
        """
        dx, dy = VALID_DIRECTIONS[direction]
        player = self.players[player_id]
        current_x, current_y = player.position

        # Move continuously until hitting a wall
        while True:
            next_x, next_y = current_x + dx, current_y + dy
            if self.game_map.get_tile(next_x, next_y) == TILE_WALL:
                break

            current_tile = self.game_map.get_tile(next_x, next_y)
            self._process_tile(current_tile, next_x, next_y, player)

            current_x, current_y = next_x, next_y

        # Update final position
        player.position = (current_x, current_y)

    def _process_tile(self, tile, x, y, player):
        """
        Handle what happens when a player steps on a specific tile.
        """
        if tile == TILE_STAR:
            # Collect star immediately
            player.score += 1
            self.game_map.set_tile(x, y, TILE_EMPTY)
            self.events.append({"player": player.id, "action": "collect"})

        elif tile == TILE_TRACE:
            # First step: restore trace back to star
            self.game_map.set_tile(x, y, TILE_STAR)
            self.events.append({"player": player.id, "action": "restore_trace"})

        elif tile == TILE_TRAP:
            # Trap: convert some stars to traces
            converted_count = self._convert_random_stars_to_traces(3)
            self.events.append({
                "player": player.id,
                "action": "hit_trap",
                "converted": converted_count
            })

        elif tile == TILE_ENEMY:
            # Enemy: add 5 stars to empty locations
            added_count = self._add_random_stars(5)
            self.events.append({
                "player": player.id,
                "action": "hit_enemy",
                "added": added_count
            })

        elif tile == TILE_LAVA:
            # Lava: restore all original stars
            restored_count = self._restore_all_stars()
            self.events.append({
                "player": player.id,
                "action": "hit_lava",
                "restored": restored_count
            })

    def _convert_random_stars_to_traces(self, count):
        """
        Randomly convert up to `count` stars (*) to traces (@).
        """
        star_positions = self.game_map.find_all(TILE_STAR)
        selected = random.sample(star_positions, min(count, len(star_positions)))
        for x, y in selected:
            self.game_map.set_tile(x, y, TILE_TRACE)
        return len(selected)

    def _add_random_stars(self, count):
        """
        Randomly add up to `count` stars (*) to empty tiles (.).
        """
        empty_positions = self.game_map.find_all(TILE_EMPTY)
        selected = random.sample(empty_positions, min(count, len(empty_positions)))
        for x, y in selected:
            self.game_map.set_tile(x, y, TILE_STAR)
        return len(selected)

    def _restore_all_stars(self):
        """
        Restore all original star positions that are currently empty.
        """
        restored = 0
        for x, y in self.game_map.original_star_positions:
            if self.game_map.get_tile(x, y) == TILE_EMPTY:
                self.game_map.set_tile(x, y, TILE_STAR)
                restored += 1
        return restored

    def check_win_condition(self):
        """
        Check if enough stars have been truly collected (i.e., removed from map),
        and if any player has scored enough to win.

        A player wins only if:
        - They have collected at least 80% of original stars (by score)
        - AND the map reflects that enough stars have been removed
        """
        total_initial = len(self.game_map.original_star_positions)
        required_to_win = int(total_initial * 0.8)

        current_remaining = len(self.game_map.find_all(TILE_STAR))
        collected_globally = total_initial - current_remaining

        for player in self.players.values():
            if player.score >= required_to_win and collected_globally >= required_to_win:
                return player.id  # Winner
        return None
