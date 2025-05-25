# common/network.py

import socket
import json
from utils.logger import Logger

class NetworkSocket:
    """
    High-level socket wrapper to handle newline-delimited JSON messages.
    """
    def __init__(self, conn, addr=None, logger=None):
        self.conn = conn
        self.addr = addr or "<unknown>"
        self.buffer = ""
        self.logger = logger or Logger("NET", log_level="INFO")
        self.conn.settimeout(1.0)

    def recv_message(self):
        """
        Receive one JSON message terminated by \n.
        Returns a dict or None if connection is closed or incomplete.
        """
        try:
            data = self.conn.recv(1024).decode()
            if not data:
                self.logger.warn(f"[{self.addr}] connection closed.")
                return None

            self.buffer += data
            while "\n" in self.buffer:
                line, self.buffer = self.buffer.split("\n", 1)
                try:
                    message = json.loads(line)
                    self.logger.debug(f"[{self.addr}] Received: {message}")
                    return message
                except json.JSONDecodeError as e:
                    self.logger.error(f"JSON decode error: {e}")
        except socket.timeout:
            return None
        except Exception as e:
            self.logger.error(f"recv_message() error: {e}")
            return None

    def send_message(self, msg_type, payload):
        """
        Send a structured message (with type/payload).
        """
        try:
            raw = json.dumps({"type": msg_type, "payload": payload}) + "\n"
            self.conn.sendall(raw.encode())
            self.logger.debug(f"[{self.addr}] Sent: {msg_type}")
        except Exception as e:
            self.logger.error(f"send_message() error: {e}")

    def send_raw(self, obj):
        """
        Send raw JSON-serializable object.
        """
        try:
            raw = json.dumps(obj) + "\n"
            self.conn.sendall(raw.encode())
            self.logger.debug(f"[{self.addr}] Sent raw object")
        except Exception as e:
            self.logger.error(f"send_raw() error: {e}")

    def close(self):
        try:
            self.conn.close()
            self.logger.info(f"[{self.addr}] Connection closed.")
        except Exception as e:
            self.logger.error(f"Error while closing connection: {e}")


# --- Server utilities ---

def create_server(host, port, backlog=5, logger=None):
    """
    Create a server socket ready to accept connections.
    """
    logger = logger or Logger("NET-SERVER")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(backlog)
        logger.info(f"Server socket created at {host}:{port}")
        return s
    except Exception as e:
        logger.error(f"Failed to create server socket: {e}")
        raise


def accept_connection(server_socket, logger=None):
    """
    Accept a new connection and wrap it in NetworkSocket.
    """
    logger = logger or Logger("NET-ACCEPT")
    try:
        conn, addr = server_socket.accept()
        logger.info(f"Accepted connection from {addr}")
        return NetworkSocket(conn, addr, logger)
    except Exception as e:
        logger.error(f"accept_connection() failed: {e}")
        return None
