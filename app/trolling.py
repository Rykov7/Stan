from .config import bot
from telebot import types
from urllib import parse


@bot.message_handler(commands=['tsya'])
def send_tsya_link(message: types.Message):
    """ тся/ться """
    link = '<a href="https://tsya.ru/">-тся/-ться</a>'
    if message.reply_to_message:
        bot.reply_to(message.reply_to_message, link, parse_mode='HTML', disable_web_page_preview=True)


@bot.message_handler(commands=['g'])
def google_it(message: types.Message):
    """ Google it! """
    if message.reply_to_message.text:
        search = parse.quote_plus(message.reply_to_message.text)
        bot.reply_to(message.reply_to_message, f"https://www.google.ru/search?q={search}", parse_mode='HTML',
                     disable_web_page_preview=True)


def check_unwanted_list(type_message: types.Message) -> bool:
    """ Check for bloggers. """
    unwanted_phrases = ['дудар', 'хауди', 'dudar']
    for phrase in unwanted_phrases:
        if phrase in type_message.text.casefold():
            return True


@bot.message_handler(func=check_unwanted_list)
def unwanted_mentions(message: types.Message):
    """ Reply to unwanted mentions. """
    bot.reply_to(message, f'У нас таких не любят! 🥴', parse_mode='HTML')
