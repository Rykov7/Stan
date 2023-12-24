import re
import string

from telebot import types

LOG_TEXT = "[%s] %s: %s"
LOG_COMM = "[%s] [%s] %s: %s"
LOGGING_LEVEL_DEBUG = 10
LOGGING_LEVEL_INFO = 20
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

RUS = """ёйцукенгшщзхъфывапролджэячсмитьбю.Ё!"№;%:?ЙЦУКЕНГШЩЗХЪ/ФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"""
ONLY_RUS_LETTERS = "ёйцукенгшщзхъфывапролджэячсмитьбю"
ONLY_ENG_LETTERS = string.ascii_lowercase
ENG = """`qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?"""
RUS_ENG_TABLE = str.maketrans(RUS, ENG)
ENG_RUS_TABLE = str.maketrans(ENG, RUS)

RULES = types.InlineKeyboardButton("🟡 Правила чата", url="https://telegra.ph/pythonchatru-07-07")
FAQ = types.InlineKeyboardButton("🔵 Частые вопросы", url="https://telegra.ph/faq-10-07-4")
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
        'зароботку', 'Набuраю', 'цuфр', 'Обучу вас', 'прuб', 'остались курсы', 'Crypt', 'kр', 'рu',
        'в лc'}

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

RULES_TEXT = (
    "Админ всегда прав и предупреждает один раз",
    "Запрещена брань, реклама, голосовые сообщения, флуд, мета-вопросы и тема ChatGPT",
    "Языки общения: русский или английский",
    "Придерживайся общепринятых норм беседы: без оскорблений, расизма, CAPS'а, политических, религиозных и взрослых тем.",
    "Знаки препинания важны, особенно вопросительный знак",
    "Твой ник должен быть читаемым и понятным",
    "Мы приветствуем общение по широкому кругу тем, но стоит придерживаться IT и Python, обсуждение прочих тем только в субботу.",
    "Прежде, чем задать вопрос, поищи ответ в интернете.",
    "Более пяти строк кода нужно присылать nekobin-ссылкой с расширением .py.",
    "Не нужно писать в ЛС.",
)

LUTZ_ID = "BQACAgQAAxkBAAPBYsWJG9Ml0fPrnbU9UyzTQiQSuHkAAjkDAAIstCxSkuRbXAlcqeQpBA"
BDMTSS_ID = "AwACAgIAAxkBAAIJrWOg2WUvLwrf7ahyJxQHB8_nqllwAAL5JQAC2_IJSbhfQIO5YnVmLAQ"
