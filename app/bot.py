import telebot
from telebot import util
from flask import Flask, request, abort
from datetime import datetime as dt
from os.path import exists
import csv

from .query_log import logging
from .me import get_me
from .config import bot, ADMIN_ID, TOKEN
from . import reminder

# https://core.telegram.org/bots/api Telegram Bot API


app = Flask(__name__)

print(">>> LutzBot is running! <<<")


@bot.message_handler(commands=['rules', 'faq'])
def send_lutz_command(message):
    bot.send_message(message.chat.id,
                     '<b>🟡 <u><a href="https://telegra.ph/pythonchatru-07-07">Правила чата</a></u></b>',
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
                     '📚 <b><u><a href="https://telegra.ph/what-to-read-10-06">Библиотека питониста</a></u></b>\n'
                     'Список рекомендуемой чатом литературы.',
                     parse_mode='HTML',
                     disable_notification=True,
                     disable_web_page_preview=True,
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


@bot.inline_handler(lambda query: len(query.query) == 0)
def default_query(inline_query):
    """Inline Aricles"""
    lutz_rus = telebot.types.InlineQueryResultCachedDocument(
        id='44', title='📕 Изучаем Python 🇷🇺',
        document_file_id='BQACAgIAAxkBAAIBcGLHE2ryQewEP1ddXOd_jF3OOHUfAAISIAACaOk4SissgGKstQbqKQQ',
        description='Марк Лутц, 5-е издание, Том 1',
        caption="""<i><b>Изучаем Python</b>, 5-е издание</i>
    ├ Автор: Марк Лутц
    └ Год: 2019""",
        parse_mode='HTML',
    )

    matthes_rus = telebot.types.InlineQueryResultCachedDocument(
        id='45', title='📕 Изучаем Python 🇷🇺',
        document_file_id='BQACAgIAAxkBAAIBdmLHF0InnLNlQuKzi1fZOYWOdu7eAAIrIAACaOk4StPj0vlMzwe2KQQ',
        description='Эрик Мэтиз , 3-е издание',
        caption="""<i><b>Изучаем Python</b>, 3-е издание</i>
    ├ Автор: Эрик Мэтиз
    └ Год: 2020""",
        parse_mode='HTML',
    )

    lutz = telebot.types.InlineQueryResultDocument(
        id='1', title='📕 Learning Python ⭐️',
        document_url='https://fk7.ru/books/OReilly.Learning.Python.5th.Edition.pdf',
        description='Mark Lutz, 5th Edition',
        caption="""<i><b>Learning Python</b>, 5th Edition</i>
    ├ by Mark Lutz
    └ Released June 2013""",
        parse_mode='HTML',
        mime_type='application/pdf',
        thumb_url='https://fk7.ru/books/OReilly.Learning.Python.5th.Edition.jpg', )

    matthes = telebot.types.InlineQueryResultDocument(
        id='2', title='📕 Python Crash Course',
        document_url='https://fk7.ru/books/PythonCrashCourse.pdf',
        description='Eric Matthes, 2th Edition',
        caption="""<i><b>Python Crash Course</b>, 2th Edition</i>
    ├ by Eric Matthes
    └ Released 2019""",
        parse_mode='HTML',
        mime_type='application/pdf',
        thumb_url='https://fk7.ru/books/PythonCrashCourse.jpg', )

    bot.answer_inline_query(
        inline_query.id, [lutz, matthes, lutz_rus, matthes_rus],
        cache_time=10)


@bot.message_handler(content_types=['document'])
def command_me(message):
    """ GetMe Informer. """
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, message.document)


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
    """ Set webhook. """
    bot.set_webhook(f'https://fk7.ru/bot{TOKEN}/', allowed_updates=util.update_types)
    """ Parse POST requests from Telegram. """
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)
