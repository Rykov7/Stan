import os
from telebot import TeleBot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('LUTZPYBOT', 'Token not in ENVIRON')
bot = TeleBot(TOKEN)

ADMIN_ID = 280887861  # t.me/Rykov7
PYTHONCHATRU = -1001338616632  # t.me/pythonchatru
