import os
import re
from telebot import TeleBot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('LUTZPYBOT', 'Token not in ENVIRON')
bot = TeleBot(TOKEN)

ADMIN_ID = 280887861  # Rykov7
PYTHONCHATRU = -1001338616632  # pythonchatru
TEST_CHAT = -1001622893830

URL_RX = re.compile(r'\w+\.\w+/\w+')
ALLOWED_WORDS = ['pastebin', 'github', 'google', 'nometa', 'python',
                 'stackoverflow', 'habr', 'medium', 'youtube']
