import threading
import time

from game.logic import GameLogic
from game.player import Player
from game.game_map import GameMap
from game.map_loader import load_map
from common.constants import VALID_DIRECTIONS
from common.network import create_server, accept_connection, NetworkSocket
from utils.logger import Logger

# --- Configuration ---
HOST = "0.0.0.0"
PORT = 9009
TICK_INTERVAL = 0.25
LEVEL = 1

log = Logger("SERVER", log_level="DEBUG")

# --- Load map from file ---
try:
    map_data = load_map(LEVEL)
except Exception as e:
    log.error(f"Failed to load map for level {LEVEL}: {e}")
    raise SystemExit(1)

# --- Init game ---
game_map = GameMap(map_data)
game_logic = GameLogic(game_map)
clients = {}
lock = threading.Lock()

def assign_player_id():
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if char not in game_logic.players:
            return char
    raise Exception("Too many players")

def find_spawn_position():
    for y, row in enumerate(game_map.grid):
        for x, tile in enumerate(row):
            if tile == ".":
                return (x, y)
    return (1, 1)

def handle_client(net: NetworkSocket):
    player_id = None
    try:
        while True:
            msg = net.recv_message()
            if msg is None:
                break

            if msg["type"] == "join":
                name = msg["payload"]["name"]
                player_id = assign_player_id()
                spawn = find_spawn_position()
                player = Player(player_id, name, spawn)

                with lock:
                    game_logic.add_player(player)
                    game_map.set_tile(spawn[0], spawn[1], player_id)
                    clients[player_id] = net

                log.info(f"Player {name} joined as {player_id} at {spawn}")
                net.send_message("init", {
                    "player_id": player_id,
                    "map": game_map.as_string_list()
                })

            elif msg["type"] == "move" and player_id:
                direction = msg["payload"].get("dir")
                if direction in VALID_DIRECTIONS:
                    with lock:
                        game_logic.handle_move(player_id, direction)
                        log.debug(f"{player_id} moved {direction}")

    except Exception as e:
        log.error(f"Client error: {e}")
    finally:
        log.warn(f"Disconnect: {player_id}")
        with lock:
            if player_id in game_logic.players:
                pos = game_logic.players[player_id].position
                game_map.set_tile(pos[0], pos[1], ".")
                del game_logic.players[player_id]
            clients.pop(player_id, None)
        net.close()

def broadcast(message):
    for pid, net in list(clients.items()):
        try:
            net.send_raw(message)
        except Exception as e:
            log.error(f"Broadcast to {pid} failed: {e}")

def game_loop():
    while True:
        time.sleep(TICK_INTERVAL)
        with lock:
            msg = {
                "type": "update",
                "payload": {
                    "map": game_map.as_string_list(),
                    "players": {pid: {"score": p.score} for pid, p in game_logic.players.items()},
                    "events": game_logic.events
                }
            }
            game_logic.events = []
        broadcast(msg)

def main():
    log.info(f"Launching game server for level {LEVEL} at {HOST}:{PORT}")
    server_sock = create_server(HOST, PORT)

    threading.Thread(target=game_loop, daemon=True).start()

    try:
        while True:
            net = accept_connection(server_sock, logger=Logger("CONN"))
            if net:
                threading.Thread(target=handle_client, args=(net,), daemon=True).start()
    except KeyboardInterrupt:
        log.warn("Server shutdown requested.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    main()
