# --------------------------
# FILE: network.py
# Purpose: Handles TCP communication using JSON
# --------------------------

import json
import socket

class NetworkSocket:
    def __init__(self, sock, label="", logger=None):
        self.sock = sock
        self.label = label
        self.logger = logger
        self.buffer = b""

    def log(self, level, msg):
        if self.logger:
            getattr(self.logger, level.lower())(f"[{self.label}] {msg}")

    def send_message(self, msg_type, payload=None):
        data = {
            "type": msg_type,
            "payload": payload or {}
        }
        try:
            raw = json.dumps(data).encode("utf-8") + b"\n"
            self.sock.sendall(raw)
            self.log("debug", f"Sent: {msg_type}")
        except Exception as e:
            self.log("error", f"Failed to send: {e}")

    def send_raw(self, data):
        try:
            raw = json.dumps(data).encode("utf-8") + b"\n"
            self.sock.sendall(raw)
            self.log("debug", "Sent raw")
        except Exception as e:
            self.log("error", f"Failed to send raw: {e}")

    def recv_message(self):
        try:
            while b"\n" not in self.buffer:
                chunk = self.sock.recv(4096)
                if not chunk:
                    self.log("warn", "connection closed.")
                    return "__DISCONNECTED__"
                self.buffer += chunk

            line, self.buffer = self.buffer.split(b"\n", 1)
            msg = json.loads(line.decode("utf-8"))
            self.log("debug", f"Received: {msg}")
            return msg
        except Exception as e:
            self.log("error", f"recv_message() error: {e}")
            return "__DISCONNECTED__"

    def close(self):
        try:
            self.sock.close()
            self.log("info", "Closed")
        except Exception as e:
            self.log("error", f"Close failed: {e}")
