import logging
import os
from urllib.error import URLError
from urllib.request import urlopen

from dotenv import load_dotenv
from telebot import logger

load_dotenv()

TOKEN = os.environ.get("LUTZPYBOT")
if not TOKEN:
    raise LookupError("LUTZPYBOT (token) has not been found in .env")

WHITEIDS = {int(i) for i in os.environ.get("whiteids").split(",")}
ROLLBACK = {int(i) for i in os.environ.get("rollback").split(",")}
USE_REMINDER = os.environ.get("use_reminder", "TRUE") == "TRUE"

RULES_URL = os.environ.get("rules_url", "https://telegra.ph/pythonchatru-07-07")
try:
    assert urlopen(RULES_URL).status == 200
except (URLError, AssertionError):
    raise LookupError(f"LUTZPYBOT rules url({RULES_URL}) is not reachable")

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger.setLevel(logging.DEBUG)
