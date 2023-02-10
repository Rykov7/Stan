""" Stan's commands and reactions. """
import random
from time import sleep
from .config import bot, types
from .filters import is_white, is_nongrata


def speak(chance_of):
    number = random.randint(0, chance_of)
    if number == 0:
        return random.choice([i.rstrip() for i in open('Stan.txt', 'r', encoding='utf8') if i])


def send_quote(after_sec, message, quote):
    """ Pretend Reading, pretend Typing, send. """
    if message.text:
        sleep(len(message.text) * 0.13 / 4)  # Reading time is quarter of the same text writing time
    bot.send_chat_action(message.chat.id, action='typing')
    sleep(after_sec)  # Typing time
    bot.send_message(message.chat.id, quote)


@bot.message_handler(func=is_white, commands=['add'])
def add_stan_quote(message):
    if message.reply_to_message and message.reply_to_message.text:
        with open('Stan.txt', 'a', encoding='utf8') as stan_quotes:
            if message.reply_to_message.text not in (i.rstrip() for i in open('Stan.txt', 'r', encoding='utf8')):
                stan_quotes.write(message.reply_to_message.text.replace('\n', ' ') + '\n')
                bot.send_message(message.chat.id,
                                 '✅ <b>Добавил</b>\n  └ <i>' + message.reply_to_message.text.replace("\n",
                                                                                                     " ") + '</i>')
            else:
                bot.send_message(message.chat.id,
                                 f'⛔️ <b>Не добавил</b>, есть токое\n  └ <i>{message.reply_to_message.text}</i>')


@bot.message_handler(func=is_white, commands=['remove'])
def remove_stan_quote(message):
    if message.reply_to_message and message.reply_to_message.text:
        if message.reply_to_message.text in (i.rstrip() for i in open('Stan.txt', 'r', encoding='utf8')):
            quotes = list(open('Stan.txt', 'r', encoding='utf8'))
            with open('Stan.txt', 'w', encoding='utf8') as stan_quotes:
                quotes.remove(message.reply_to_message.text + '\n')
                stan_quotes.writelines(quotes)
            bot.send_message(message.chat.id, f'✅ <b>Удалил</b>\n  └ <i>{message.reply_to_message.text}</i>')
        else:
            bot.send_message(message.chat.id, f'⛔️ <b>Нет такого</b>\n  └ <i>{message.reply_to_message.text}</i>')


@bot.message_handler(func=is_nongrata)
def tease_nongrata(message: types.Message):
    """ Reply to non grata mentions. """
    bot.reply_to(message, f'у нас тут таких не любят')
