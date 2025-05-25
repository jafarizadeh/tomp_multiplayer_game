# client.py

import time
from common.network import NetworkSocket
from utils.logger import Logger

import socket
import threading

# --- Configuration ---
HOST = "127.0.0.1"
PORT = 9009
PLAYER_NAME = "Player"

# --- Logger ---
log = Logger("CLIENT", log_level="DEBUG")

# --- Globals ---
player_id = None
game_map = []
running = True

# --- Handle user input (WASD) ---
def input_loop(net: NetworkSocket):
    global running
    while running:
        cmd = input("Move (W/A/S/D or Q to quit): ").strip().upper()
        if cmd == "Q":
            running = False
            break
        direction = {"W": "UP", "A": "LEFT", "S": "DOWN", "D": "RIGHT"}.get(cmd)
        if direction:
            net.send_message("move", {"dir": direction})
        else:
            print("Invalid input. Use W A S D.")

# --- Print map nicely ---
def print_map(map_data):
    print("\n".join(map_data))
    print("-" * len(map_data[0]))

# --- Main client logic ---
def main():
    global player_id, game_map

    # Connect to server
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        net = NetworkSocket(sock, f"{HOST}:{PORT}", logger=Logger("NET", log_level="WARN"))
    except Exception as e:
        log.error(f"Failed to connect to server: {e}")
        return

    # Send join request
    net.send_message("join", {"name": PLAYER_NAME})

    # Start input loop in background
    threading.Thread(target=input_loop, args=(net,), daemon=True).start()

    try:
        while running:
            msg = net.recv_message()
            if msg is None:
                continue

            if msg["type"] == "init":
                player_id = msg["payload"]["player_id"]
                game_map = msg["payload"]["map"]
                print_map(game_map)
                log.info(f"Joined as player {player_id}")

            elif msg["type"] == "update":
                game_map = msg["payload"]["map"]
                players = msg["payload"]["players"]
                events = msg["payload"]["events"]

                print_map(game_map)
                print(f"Your ID: {player_id} | Score: {players.get(player_id, {}).get('score', 0)}")
                for e in events:
                    if e.get("player") == player_id:
                        log.info(f"Event: {e['action']}")

            time.sleep(0.05)

    except KeyboardInterrupt:
        log.warn("Client shutting down (Ctrl+C)")
    finally:
        running = False
        net.close()

if __name__ == "__main__":
    main()
