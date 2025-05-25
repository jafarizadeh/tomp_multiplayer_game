import socket
import json
from utils.logger import Logger

class NetworkSocket:
    """
    A high-level wrapper around socket to send/receive JSON messages.
    Designed for newline-delimited TCP communication.
    """

    def __init__(self, conn, addr=None, logger=None):
        self.conn = conn
        self.addr = addr or "<unknown>"
        self.buffer = ""
        self.logger = logger or Logger("NET", log_level="INFO")

    def recv_message(self):
        """
        Receive one full JSON message from the buffer.
        Messages must end with newline \n.
        Returns the parsed JSON object or None if no complete message available.
        """
        try:
            data = self.conn.recv(1024).decode()
            if not data:
                self.logger.warn(f"[{self.addr}] Connection closed by client.")
                return None

            self.buffer += data

            while "\n" in self.buffer:
                line, self.buffer = self.buffer.split("\n", 1)
                try:
                    msg = json.loads(line)
                    self.logger.debug(f"[{self.addr}] Received: {msg}")
                    return msg
                except json.JSONDecodeError as e:
                    self.logger.error(f"[{self.addr}] JSON decode error: {e}")
                    continue

        except socket.timeout:
            self.logger.warn(f"[{self.addr}] Timeout occurred.")
            return None
        except Exception as e:
            self.logger.error(f"[{self.addr}] recv_message() error: {e}")
            return None

    def send_message(self, msg_type, payload):
        """
        Send a structured JSON message (type + payload).
        """
        try:
            message = {
                "type": msg_type,
                "payload": payload
            }
            raw = json.dumps(message) + "\n"
            self.conn.sendall(raw.encode())
            self.logger.debug(f"[{self.addr}] Sent: {msg_type}")
        except Exception as e:
            self.logger.error(f"[{self.addr}] send_message() error: {e}")

    def send_raw(self, obj):
        """
        Send any arbitrary JSON-serializable object.
        """
        try:
            raw = json.dumps(obj) + "\n"
            self.conn.sendall(raw.encode())
            self.logger.debug(f"[{self.addr}] Sent raw object")
        except Exception as e:
            self.logger.error(f"[{self.addr}] send_raw() error: {e}")

    def close(self):
        """
        Close the underlying socket connection.
        """
        try:
            self.conn.close()
            self.logger.info(f"[{self.addr}] Connection closed")
        except Exception as e:
            self.logger.error(f"[{self.addr}] Error closing connection: {e}")
