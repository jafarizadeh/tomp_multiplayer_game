# --------------------------
# FILE: logic.py
# Purpose: Core game logic engine
# --------------------------

from common.constants import *
from utils.logger import Logger

log = Logger("GAME_LOGIC", log_level="DEBUG")

class GameLogic:
    def __init__(self, game_map):
        self.game_map = game_map
        self.players = {}  # {player_id: Player}
        self.events = []
        log.debug("GameLogic initialized.")

    def add_player(self, player):
        self.players[player.id] = player
        self.game_map.set_tile(*player.position, player.id)
        log.info(f"Player {player.name} ({player.id}) added to game logic at {player.position}.")

    def handle_move(self, player_id, direction):
        log.debug(f"handle_move called with player_id={player_id}, direction={direction}")

        if player_id not in self.players:
            log.warn(f"Invalid move: unknown player_id {player_id}")
            return

        dx, dy = VALID_DIRECTIONS.get(direction, (0, 0))
        log.debug(f"Direction deltas: dx={dx}, dy={dy}")

        player = self.players[player_id]
        x, y = player.position
        nx, ny = x + dx, y + dy
        log.debug(f"Player {player_id} current position: ({x},{y}) → target: ({nx},{ny})")

        if not self.game_map.in_bounds(nx, ny):
            log.debug(f"Out of bounds move blocked for ({nx},{ny}).")
            return

        tile = self.game_map.get_tile(nx, ny)
        log.debug(f"Tile at ({nx},{ny}) is '{tile}'")

        if tile == TILE_WALL:
            log.debug("Move blocked by wall.")
            return

        if tile == TILE_STAR:
            log.debug(f"{player_id} collected a star at ({nx},{ny})")
            player.add_score(1)
            self.events.append({"player": player_id, "action": "collected_star"})
            log.info(f"{player_id} collected a star. Score: {player.score}")

        # Update map
        self.game_map.set_tile(x, y, TILE_EMPTY)
        player.move_to((nx, ny))
        log.debug(f"Updated position for {player_id}: {player.position}")
        self.game_map.set_tile(nx, ny, player.id)
        log.debug(f"Tile at ({x},{y}) set to '{TILE_EMPTY}', tile at ({nx},{ny}) set to '{player.id}'")

    def get_state(self):
        log.debug("get_state called.")
        return {
            "map": self.game_map.as_string_list(),
            "players": {pid: {"score": p.score} for pid, p in self.players.items()},
            "events": self.events
        }
