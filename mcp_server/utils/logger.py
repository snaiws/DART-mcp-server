import logging
import time
from pathlib import Path
import os


class TimeSizeRotatingHandler(logging.Handler):
    def __init__(self, path: Path, max_bytes=100* 1024*1024, interval_sec=604800):
        super().__init__()
        self.path = path
        self.max_bytes = max_bytes
        self.interval_sec = interval_sec
        self.last_rotated = time.time()
        self.base_path = path
        self.suffix_count = 0
        Path(self.base_path).parent.mkdir(parents=True, exist_ok=True)

    def emit(self, record):
            now = time.time()
            msg = self.format(record) + "\n"

            # Check time-based rotation
            if now - self.last_rotated > self.interval_sec:
                self._rotate()
                self.last_rotated = now
            # Check size-based rotation
            elif os.path.exists(self.base_path) and os.path.getsize(self.base_path) > self.max_bytes:
                self._rotate()
            
            # Write the log message to file
            with open(self.base_path, 'a', encoding='utf-8') as f:
                f.write(msg)

    def _rotate(self):
        rotated_name = f"{self.base_path}.{self.suffix_count}"
        os.rename(self.base_path, rotated_name)
        self.suffix_count += 1

# ======= Logger Setup =======

def setup_logger(name: str, log_path,
                 level=logging.INFO,
                 max_bytes=100 * 1024 * 1024,
                 interval_sec=604800):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = TimeSizeRotatingHandler(log_path, max_bytes=max_bytes, interval_sec=interval_sec)
    formatter = logging.Formatter('{asctime} | {name} | {funcName} | {levelname} | {message}', 
                                 '%Y-%m-%d %H:%M:%S', 
                                 style='{')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger