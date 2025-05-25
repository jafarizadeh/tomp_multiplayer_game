# --------------------------
# FILE: client.py
# Purpose: Multiplayer game client
# --------------------------

import socket
from common.network import NetworkSocket
from utils.logger import Logger

HOST = "127.0.0.1"
PORT = 9009
PLAYER_NAME = "Player"

log = Logger("CLIENT", log_level="DEBUG")

def print_map(map_data):
    print("\n" + "=" * 20)
    print("\n".join(map_data))
    print("=" * 20)

def main():
    running = True
    player_id = None
    game_map = []

    log.info(f"Connecting to server at {HOST}:{PORT}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        net = NetworkSocket(sock, f"{HOST}:{PORT}", logger=log)
    except Exception as e:
        log.error(f"Connection failed: {e}")
        return

    net.send_message("join", {"name": PLAYER_NAME})

    try:
        while running:
            msg = net.recv_message()
            if msg == "__DISCONNECTED__":
                log.warn("Disconnected from server.")
                break
            if msg is None:
                continue

            if msg["type"] == "init":
                player_id = msg["payload"]["player_id"]
                game_map = msg["payload"]["map"]
                log.info(f"Joined as player {player_id}")
                print_map(game_map)

            elif msg["type"] == "update":
                game_map = msg["payload"]["map"]
                players = msg["payload"]["players"]
                print_map(game_map)
                log.info(f"Your ID: {player_id} | Score: {players.get(player_id, {}).get('score', 0)}")

                while True:
                    cmd = input("Move (W/A/S/D or Q to quit): ").strip().lower()
                    if cmd == "q":
                        running = False
                        return
                    if cmd in ["w", "a", "s", "d"]:
                        log.debug(f"Sending move: {cmd}")
                        net.send_message("move", {"dir": cmd})
                        break
                    else:
                        log.warn("Invalid input. Use W/A/S/D or Q.")

    except KeyboardInterrupt:
        log.warn("Client interrupted.")
    except Exception as e:
        import traceback
        log.error(f"Unhandled error: {e}\n{traceback.format_exc()}")
    finally:
        net.close()
        log.info("Client shutdown.")

if __name__ == "__main__":
    main()
