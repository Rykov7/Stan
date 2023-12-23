import logging
import os

from dotenv import load_dotenv
from telebot import logger

from .helpers import is_url_reachable

load_dotenv()

TOKEN = os.environ.get("LUTZPYBOT")
if not TOKEN:
    raise LookupError("LUTZPYBOT (token) has not been found in .env")

WHITEIDS = {int(i) for i in os.environ.get("whiteids").split(",")}
ROLLBACK = {int(i) for i in os.environ.get("rollback").split(",")}
USE_REMINDER = os.environ.get("use_reminder", "TRUE") == "TRUE"

RULES_URL = os.environ.get("rules_url", "https://telegra.ph/pythonchatru-07-07")
if not is_url_reachable(RULES_URL):
    raise LookupError(f"LUTZPYBOT rules url({RULES_URL}) is not reachable")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger.setLevel(logging.INFO)
