import os
import re
from telebot import TeleBot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('LUTZPYBOT', 'Token not in ENVIRON')
bot = TeleBot(TOKEN, 'HTML', skip_pending=True, disable_web_page_preview=True, allow_sending_without_reply=True)

ADMIN_ID = 280887861  # Rykov7
PYTHONCHATRU = -1001338616632  # pythonchatru

URL_RX = re.compile(r'\w+\.\w+/\w+')
ALLOWED_WORDS = ['paste', 'github', 'google', 'nometa', 'python', 'django', 'flask', 'fastapi',
                 'stackoverflow', 'habr', 'medium', 'youtu', 'stepik', 'telegraph', '#rtfm', 'support']

WHITEUN = set(os.environ.get('whitelist', '<<<ERR_USRS').split(','))
WHITEIDS = {int(i) for i in os.environ.get('whiteids', '<<<ERR_IDS').split(',')}


RUS = """ёйцукенгшщзхъфывапролджэячсмитьбю.Ё!"№;%:?ЙЦУКЕНГШЩЗХЪ/ФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"""
ENG = """`qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?"""
RUS_ENG_TABLE = str.maketrans(RUS, ENG)
ENG_RUS_TABLE = str.maketrans(ENG, RUS)
