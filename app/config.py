import os
import re
import logging

import telebot.types
from fastapi import FastAPI
from telebot.async_telebot import AsyncTeleBot
from telebot import logger, types
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger.setLevel(logging.ERROR)

logging.warning("[START] Stan")

load_dotenv()

TOKEN = os.environ.get("LUTZPYBOT")
if not TOKEN:
    raise LookupError("LUTZPYBOT (token) has not been found in .env")

bot = AsyncTeleBot(
    TOKEN,
    "HTML",
    disable_web_page_preview=True,
    allow_sending_without_reply=True,
    colorful_logs=True,
)
LOG_TEXT = "[%s] %s: %s"
LOG_COMM = "[%s] [%s] %s: %s"
app = FastAPI(docs=None, redoc_url=None)

DATA = "data/chat"

ADMIN_ID = 280887861  # Rykov7
PYTHONCHATRU = -1001338616632  # pythonchatru

URL_RX = re.compile(r"\w+\.\w+/(\+)?\w+")
ALLOWED_WORDS = [
    "paste",
    "nekobin",
    "github",
    "google",
    "nometa",
    "python",
    "django",
    "flask",
    "fastapi",
    "wiki",
    "stackoverflow",
    "rykov7",
    "habr",
    "medium",
    "youtu",
    "rutube",
    "stepik",
    "digitalocean",
    "gra.ph",
    "#rtfm",
    "support",
    "jetbrains",
]

WHITEIDS = {int(i) for i in os.environ.get("whiteids").split(",")}
ROLLBACK = {int(i) for i in os.environ.get("rollback").split(",")}

RUS = """ёйцукенгшщзхъфывапролджэячсмитьбю.Ё!"№;%:?ЙЦУКЕНГШЩЗХЪ/ФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"""
ENG = """`qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?"""
RUS_ENG_TABLE = str.maketrans(RUS, ENG)
ENG_RUS_TABLE = str.maketrans(ENG, RUS)

RULES = types.InlineKeyboardButton(
    "🟡 Правила чата", url="https://telegra.ph/pythonchatru-07-07"
)
FAQ = types.InlineKeyboardButton(
    "🔵 Частые вопросы", url="https://telegra.ph/faq-10-07-4"
)
LIB = types.InlineKeyboardButton("📚 Книги", url="https://telegra.ph/what-to-read-10-06")

SPAM = {"me.sv/", "tg.sv/", "goo.by/", "go.sv/", "intim.video/", "uclck.ru/", 'раб0т',
        '0плат', 'Жду в ЛС', 'новый способ заработка', 'криптовалют', 'цифровых валют',
        'Binance', 'ByBit', 'Помогу заработать', 'подробнее в лс', 'арбитраж', 'напиши в личку',
        'DEX бирж', 'пишите в ЛС', 'Писать в ЛИЧКУ!', 'любую девушку', 'Пишите в личку',
        'прибыль у вaс', 'обучaю быстро', 'в л.с.', 'вопросам в ЛС', 'Предлагаю новый вид заработка',
        'пишите мне в ЛС', 'Писать в ЛС', 'межбиржев', 'КУПЮРЫ', '💎', 'kрипт', 'биpж', 'apбитpaж',
        'в неделю выходит до', 'предложить заработок', 'голые фот', '🔞', 'интимные фот', '➡️',
        'заработка в крипте', 'Веду набор', 'Идёт набор', 'мне в ЛС', 'Доход от', 'Trading',
        'P2P', 'Идет набор', 'в лс', 'нaбop', 'комaндy', 'kpuпт', 'бupж', '💰', 'пишитe', '💸',
        '$ в неделю', 'обучаю с нуля', 'доходы для всех', 'по трейдингу', 'фальшивые рубли', '‼️',
        'зароботку', 'Набuраю', 'цuфр', 'Обучу вас', 'прuб', 'остались курсы', 'Crypt', 'kр', 'рu'}
NON_GRATA = {"дудар", "хауди", "dudar"}
BAN_WORDS = {"GREEN"}

ZEN = [
    "Beautiful is better than ugly.",
    "Explicit is better than implicit.",
    "Simple is better than complex.",
    "Complex is better than complicated.",
    "Flat is better than nested.",
    "Sparse is better than dense.",
    "Readability counts.",
    "Special cases aren't special enough to break the rules. Although practicality beats purity.",
    "Errors should never pass silently. Unless explicitly silenced.",
    "In the face of ambiguity, refuse the temptation to guess.",
    "There should be one — and preferably only one — obvious way to do it.",
    "Now is better than never. Although never is often better than *right* now.",
    "If the implementation is hard to explain, it's a bad idea.",
    "If the implementation is easy to explain, it may be a good idea.",
    "Namespaces are one honking great idea — let's do more of those!",
]

