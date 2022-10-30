from telebot import types
from flask import Flask, request, abort
from datetime import datetime as dt
from os.path import exists
import csv
from time import sleep
from threading import Thread

from .query_log import logging
from .me import get_me
from .config import bot, ADMIN_ID, TOKEN
from . import reminder

# https://core.telegram.org/bots/api Telegram Bot API
# https://github.com/eternnoir/pyTelegramBotAPI/tree/master/examples


app = Flask(__name__)

print(">>> LutzBot is running! <<<")

zen_rows = ['Beautiful is better than ugly.', 'Explicit is better than implicit.', 'Simple is better than complex.',
            'Complex is better than complicated.', 'Flat is better than nested.', 'Sparse is better than dense.',
            'Readability counts.',
            "Special cases aren't special enough to break the rules. Although practicality beats purity.",
            'Errors should never pass silently. Unless explicitly silenced.',
            'In the face of ambiguity, refuse the temptation to guess.',
            'There should be one — and preferably only one — obvious way to do it.',
            'Now is better than never. Although never is often better than *right* now.',
            "If the implementation is hard to explain, it's a bad idea.",
            'If the implementation is easy to explain, it may be a good idea.',
            "Namespaces are one honking great idea — let's do more of those!"]


def wait_for_readers(action, chat_id, msg_id):
    sleep(60)
    action(chat_id, msg_id)


@bot.message_handler(func=(lambda message: message.text.startswith('https://tg.sv/') or
                                           message.text.startswith('https://goo.by/') or
                                           message.text.startswith('🍀GREEN ROOM🍀')),
                     content_types=['animation', 'text'])
def moderate_messages(message: types.Message):
    warn = bot.send_message(message.chat.id,
                            f'♻ <b><a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a></b>'
                            f' заблокирован.', parse_mode='HTML')
    bot.ban_chat_member(message.chat.id, message.from_user.id)
    bot.delete_message(message.chat.id, message.id)

    Thread(target=wait_for_readers, args=(bot.delete_message, message.chat.id, warn.id)).start()


@bot.message_handler(commands=['rules'])
def send_lutz_command(message):
    bot.send_message(message.chat.id,
                     '<b>🟡 <u><a href="https://telegra.ph/pythonchatru-07-07">Правила чата</a></u></b>',
                     parse_mode='HTML',
                     disable_notification=True,
                     )
    logging(message)


@bot.message_handler(commands=['faq'])
def send_lutz_command(message):
    bot.send_message(message.chat.id,
                     '<b>🔵 <u><a href="https://telegra.ph/faq-10-07-4">FAQ</a></u></b>',
                     parse_mode='HTML',
                     disable_notification=True,
                     )
    logging(message)


@bot.message_handler(commands=['lutz'])
def send_lutz_command(message):
    bot.send_document(
        message.chat.id,
        document='BQACAgQAAxkBAAPBYsWJG9Ml0fPrnbU9UyzTQiQSuHkAAjkDAAIstCxSkuRbXAlcqeQpBA',
        caption="""<i><b>Learning Python</b>, 5th Edition</i>
    ├ by Mark Lutz
    └ Released June 2013""",
        parse_mode='HTML')
    logging(message)


@bot.message_handler(commands=['lib', 'library', 'book', 'books'])
def send_lutz_command(message):
    bot.send_message(message.chat.id,
                     '📚 <b><u><a href="https://telegra.ph/what-to-read-10-06">Библиотека питониста</a></u></b>',
                     parse_mode='HTML',
                     disable_notification=True,
                     )
    logging(message)


@bot.message_handler(commands=['start'])
def send_start_notify_admin(message):
    bot.send_message(
        ADMIN_ID, get_me(message), parse_mode='HTML')
    logging(message)


@bot.message_handler(commands=['log'])
def send_log(message):
    """Send log from log.csv"""
    if message.from_user.id == ADMIN_ID:
        file_path = f"logs/log_{dt.now().strftime('%Y-%m')}.csv"
        if exists(file_path):
            with open(file_path, "r", newline='', encoding='utf-8') as f:
                all_rows = list(csv.reader(f))
            text = ''
            for row in all_rows[-min(len(all_rows), 5):]:
                text += str(row) + '\n'
            bot.send_message(ADMIN_ID, f'<code>{text}</code>', parse_mode='html')


@bot.inline_handler(lambda query: True)
def default_query(inline_query):
    """Inline Texts"""
    zen = []
    for id_p, phrase in enumerate(zen_rows):
        q = inline_query.query.casefold()
        if phrase.casefold().startswith(q) or ' ' + q in phrase.casefold():
            zen.append(types.InlineQueryResultArticle(
                f"{id_p + 7000}", f'The Zen of Python #{id_p + 1}', types.InputTextMessageContent(
                    f"<i>{phrase}</i>", parse_mode='HTML'), description=phrase))

    bot.answer_inline_query(inline_query.id, zen, cache_time=12)


@bot.message_handler(commands=['me'])
def command_me(message):
    """GetMe Informer"""
    bot.send_message(message.chat.id, get_me(message), parse_mode='HTML')
    logging(message)


@bot.message_handler(commands=['remind'])
def remind_manually(message):
    """Remind manually"""
    args = message.text.split()
    if len(args) > 1:
        try:
            today = dt.strptime(args[1], "%m-%d-%Y")
        except ValueError as ve:
            bot.send_message(message.chat.id, f"Не удалось разобрать дату!\n{ve}", parse_mode='HTML')
        else:
            reminder.remind(message.chat.id, today)
    else:
        bot.send_message(message.chat.id, f"<b>Формат даты: MM-DD-YYYY</b>\n\n"
                                          f"Примеры:\n"
                                          f"/remind 09-12-2024\n"
                                          f"/remind 09-13-2022", parse_mode='HTML')


@bot.message_handler(commands=['jobs'])
def list_jobs(message):
    """List all jobs"""
    if message.chat.id == ADMIN_ID:
        text = reminder.print_get_jobs()
        bot.send_message(message.chat.id, text, parse_mode='HTML')


@app.route(f"/bot{TOKEN}/", methods=['POST'])
def webhook():
    """ Parse POST requests from Telegram. """
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)
