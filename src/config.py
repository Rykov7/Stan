import logging
import os
from collections import deque

from telebot import logger

from .helpers import is_url_reachable


TOKEN = os.environ.get("STAN")
if not TOKEN:
    raise LookupError("STAN (token) has not been found in .env")

whiteids_env = os.environ.get("whiteids")
WHITEIDS = {int(i) for i in whiteids_env.split(",")} if whiteids_env else set()

rollback_env = os.environ.get("rollback")
ROLLBACK = {int(i) for i in rollback_env.split(",")} if rollback_env else set()

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
buffer_handler.setLevel(logging.INFO)
buffer_handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
))

logging.getLogger().addHandler(buffer_handler)
