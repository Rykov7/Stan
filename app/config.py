import os
import re
import logging

import telebot.types
from flask import Flask
from telebot import TeleBot, logger, types
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
logger.setLevel(logging.INFO)

logging.warning("[START] Stan")

load_dotenv()

TOKEN = os.environ.get("LUTZPYBOT")
if not TOKEN:
    raise LookupError("LUTZPYBOT (token) has not been found in .env")

bot = TeleBot(
    TOKEN,
    "HTML",
    disable_web_page_preview=True,
    allow_sending_without_reply=True,
    colorful_logs=True,
)
LOG_TEXT = "[%s] %s: %s"
LOG_COMM = "[%s] [%s] %s: %s"
app = Flask(__name__)

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
        '0плат', 'Жду в ЛС', 'новый способ заработка', 'криптовалют', 'цифровых валют', 'кpuпт',
        'Binance', 'ByBit', 'Помогу заработать', 'подробнее в лс', 'арбитраж', 'напиши в личку',
        'DEX бирж', 'пишите в ЛС', 'Писать в ЛИЧКУ!', 'любую девушку', 'Пишите в личку',
        'прибыль у вaс', 'обучaю быстро', 'в л.с.', 'вопросам в ЛС', 'Предлагаю новый вид заработка',
        'пишите мне в ЛС', 'межбиржев', 'КУПЮРЫ', '💎', 'kрипт', 'биpж', 'apбитpaж', 'в неделю выходит до',
        'предложить заработок', 'голые фото'}
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

for white_id in WHITEIDS:
    bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("nobot", "/нобот Телебот не должен быть первым проектом"),
            telebot.types.BotCommand("nogui", "/ногуи GUI приложение не должно быть первым проектом"),
            telebot.types.BotCommand("nojob", "/ноджоб, Мы здесь не для того чтобы за тебя решать задачи"),
            telebot.types.BotCommand("nometa", "/номета Не задавайте мета-вопросов"),
            telebot.types.BotCommand("neprivet", "/непривет"),
            telebot.types.BotCommand("quote", "/цитата Случайная цитата"),
            telebot.types.BotCommand("lutz", "/лутц Прислать книгу Learning Python"),
            telebot.types.BotCommand("bdmtss", "/бдмтсс Римшот"),
            telebot.types.BotCommand("g", "/г Загуглить (аргументы или цитируемое)"),
            telebot.types.BotCommand("rules", "/правила чата (работает с аргументом-номером пункта)"),
            telebot.types.BotCommand("faq", "/чзв Частые вопросы"),
            telebot.types.BotCommand("books", "/библиотека питониста"),
            telebot.types.BotCommand("links", "/ссылки на правила, чзв и библиотеку"),
            telebot.types.BotCommand("tsya", "/тся и /ться"),
            telebot.types.BotCommand("add", "добавить цитату [Whitelist]"),
            telebot.types.BotCommand("remove", "удалить цитату [Whitelist]"),
        ],
        scope=telebot.types.BotCommandScopeChatMember(PYTHONCHATRU, white_id)
    )
