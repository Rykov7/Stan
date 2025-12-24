import logging
import os
from collections import deque

from telebot import logger

from .helpers import is_url_reachable


TOKEN = os.environ.get("STAN")
if not TOKEN:
    raise LookupError("STAN (token) has not been found in .env")

WHITEIDS = {int(i) for i in os.environ.get("whiteids").split(",")}
ROLLBACK = {int(i) for i in os.environ.get("rollback").split(",")}
USE_REMINDER = os.environ.get("use_reminder", "TRUE") == "TRUE"

RULES_URL = os.environ.get("rules_url", "https://telegra.ph/pythonchatru-07-07")
if not is_url_reachable(RULES_URL):
    raise LookupError(f"STAN rules url({RULES_URL}) is not reachable")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", force=True)
logger.setLevel(logging.ERROR)


# Лог в буфер для HTML:
log_buffer = deque(maxlen=1500)

class BufferHandler(logging.Handler):
    def emit(self, record):
        log_buffer.append(self.format(record))


buffer_handler = BufferHandler()
buffer_handler.setLevel(logging.ERROR)
buffer_handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
))

logging.getLogger().addHandler(buffer_handler)
