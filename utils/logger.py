import datetime
import sys

class Logger:
    """
    Lightweight and customizable logger for CLI-based games.
    Supports log levels, timestamps, module tags, and optional output to file.
    """

    LEVELS = ["DEBUG", "INFO", "WARN", "ERROR"]

    def __init__(self, name="LOG", enabled=True, log_level="DEBUG", to_file=False, file_path=None):
        self.name = name
        self.enabled = enabled
        self.log_level = log_level.upper()
        self.to_file = to_file
        self.file_path = file_path
        self.level_index = self.LEVELS.index(self.log_level) if self.log_level in self.LEVELS else 0

    def _now(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _should_log(self, level):
        return self.LEVELS.index(level) >= self.level_index

    def _format(self, level, message):
        return f"[{self._now()}][{self.name}][{level}] {message}"

    def _write(self, msg):
        if self.to_file and self.file_path:
            try:
                with open(self.file_path, "a", encoding="utf-8") as f:
                    f.write(msg + "\n")
            except Exception as e:
                print(f"[LOGGER][ERROR] Failed to write log to file: {e}", file=sys.stderr)
        else:
            print(msg)

    def log(self, message, level="INFO"):
        if not self.enabled or not self._should_log(level):
            return
        formatted = self._format(level, message)
        self._write(formatted)

    def debug(self, msg): self.log(msg, "DEBUG")
    def info(self, msg): self.log(msg, "INFO")
    def warn(self, msg): self.log(msg, "WARN")
    def error(self, msg): self.log(msg, "ERROR")

    def set_level(self, level):
        if level.upper() in self.LEVELS:
            self.log_level = level.upper()
            self.level_index = self.LEVELS.index(self.log_level)

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
