# --------------------------
# FILE: server.py
# Purpose: Multiplayer game server
# --------------------------

import socket
import threading
from game.map_loader import load_map
from game.game_map import GameMap
from game.logic import GameLogic
from game.player import Player
from common.network import NetworkSocket
from common.constants import PLAYER_SYMBOLS
from utils.logger import Logger

log = Logger("SERVER", log_level="DEBUG")

HOST = "0.0.0.0"
PORT = 9009
clients = {}
game_logic = None

def handle_client(net, addr):
    global game_logic
    player_id = None

    try:
        while True:
            msg = net.recv_message()
            if msg == "__DISCONNECTED__":
                log.warn(f"[{addr}] disconnected.")
                break
            if msg is None:
                continue

            log.info(f"[{addr}] Received: {msg}")

            if msg["type"] == "join":
                player_id = PLAYER_SYMBOLS[len(game_logic.players)]
                pos = game_logic.game_map.find_empty()
                player = Player(player_id, msg["payload"].get("name", player_id), pos)
                game_logic.add_player(player)
                clients[player_id] = net

                net.send_message("init", {
                    "player_id": player_id,
                    "map": game_logic.game_map.as_string_list()
                })
                log.info(f"Player {player_id} joined at {pos}")

            elif msg["type"] == "move":
                if player_id:
                    direction = msg["payload"].get("dir")
                    log.info(f"Move from {player_id}: {direction}")
                    game_logic.handle_move(player_id, direction)
                    broadcast()

    except Exception as e:
        import traceback
        log.error(f"Client error: {e}\n{traceback.format_exc()}")
    finally:
        if player_id and player_id in clients:
            del clients[player_id]
        net.close()
        log.info(f"[{addr}] Connection closed.")

def broadcast():
    state = game_logic.get_state()
    state["type"] = "update"
    for pid, net in clients.items():
        try:
            net.send_raw(state)
        except Exception as e:
            log.warn(f"Broadcast failed to {pid}: {e}")

def main():
    global game_logic
    log.info(f"Starting server on {HOST}:{PORT}")
    game_map = GameMap(load_map(1))
    game_logic = GameLogic(game_map)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    log.info(f"Server listening at {HOST}:{PORT}")

    try:
        while True:
            conn, addr = s.accept()
            log.info(f"Accepted connection from {addr}")
            net = NetworkSocket(conn, str(addr), logger=Logger("NET", log_level="DEBUG"))
            threading.Thread(target=handle_client, args=(net, addr), daemon=True).start()
    except KeyboardInterrupt:
        log.warn("Server interrupted by user.")
    finally:
        s.close()
        log.info("Server shut down.")

if __name__ == "__main__":
    main()
