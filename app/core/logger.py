import logging
from logging.handlers import RotatingFileHandler
import os

ENV = os.getenv("ENV", "development")
DEBUG_MODE = ENV == "development"

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

formatter = logging.Formatter(
    "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)

# === General App Log (all logs)
file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, 'app.log'),
    maxBytes=5 * 1024 * 1024, backupCount=5
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)  # ✅ Always log DEBUG+

# === Debug-only Log (optional, for deeper tracing)
debug_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, 'debug.log'),
    maxBytes=5 * 1024 * 1024, backupCount=3
)
debug_handler.setFormatter(formatter)
debug_handler.setLevel(logging.DEBUG)

# === Info Log (INFO and below)
class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level): self.max_level = max_level
    def filter(self, record): return record.levelno <= self.max_level

info_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, 'info.log'),
    maxBytes=5 * 1024 * 1024, backupCount=5
)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)
info_handler.addFilter(MaxLevelFilter(logging.INFO))

# === Error Log (ERROR+)
error_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, 'error.log'),
    maxBytes=5 * 1024 * 1024, backupCount=5
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

# === Console Output (less noisy in production)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)

# === Final Logger Setup
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)  # ✅ Capture all logs internally

logger.addHandler(file_handler)
logger.addHandler(debug_handler)
logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)

logger.propagate = False
