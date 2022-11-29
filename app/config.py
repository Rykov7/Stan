import os
import re
from telebot import TeleBot
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')


load_dotenv()

TOKEN = os.environ.get('LUTZPYBOT', 'Token not in ENVIRON')
bot = TeleBot(TOKEN)

ADMIN_ID = 280887861  # Rykov7
PYTHONCHATRU = -1001338616632  # pythonchatru

URL_RX = re.compile(r'\w+\.\w+/\w+')
ALLOWED_WORDS = ['pastebin', 'github', 'google', 'nometa', 'python', 'django', 'flask', 'fastapi',
                 'stackoverflow', 'habr', 'medium', 'youtube', 'stepik', 'telegraph']

WHITEUN = set(os.environ.get('whitelist', '<<<ERR_USRS').split(','))
logging.warning(f'White users {WHITEUN}')

WHITEIDS = {int(i) for i in os.environ.get('whiteids', '<<<ERR_IDS').split(',')}
logging.warning(f'White IDs {WHITEIDS}')
