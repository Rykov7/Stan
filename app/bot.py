from telebot import types
from flask import Flask, request, abort
from datetime import datetime as dt
from os.path import exists
import csv
from time import sleep
from threading import Thread
import shelve

from . import report
from .query_log import logging
from .me import get_me
from .config import bot, ADMIN_ID, TOKEN, PYTHONCHATRU
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
    """ Delete message after limited time. """
    sleep(30)
    action(chat_id, msg_id)


def check_spam_list(type_message: types.Message) -> bool:
    """ Check for mentioning unwanted persons in text. """
    unwanted_phrases = ['tg.sv', 'goo.by', 'go.sv']
    for phrase in unwanted_phrases:
        if phrase in type_message.text.casefold():
            return True


@bot.message_handler(func=check_spam_list, content_types=['text'])
def moderate_messages(message: types.Message):
    """ Ban user and delete their message. """
    warn = bot.send_message(message.chat.id,
                            f'♻ <b><a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a></b>'
                            f' заблокирован.', parse_mode='HTML')
    Thread(target=wait_for_readers, args=(bot.delete_message, message.chat.id, warn.id)).start()
    bot.ban_chat_member(message.chat.id, message.from_user.id)
    bot.delete_message(message.chat.id, message.id)

    if message.chat.id == PYTHONCHATRU:
        with shelve.open('chat_stats') as chat_stats:
            chat_stats['Banned'] += 1


@bot.message_handler(content_types=['video'])
def catch_videos(message: types.Message):
    """Catch offensive videos"""
    if message.video.file_name in ['Новый грин.mp4']:
        warn = bot.send_message(message.chat.id, f"♻ Видео {message.video.file_name} заблокировано.")
        bot.delete_message(message.chat.id, message.id)
        bot.ban_chat_member(message.chat.id, message.from_user.id)
        Thread(target=wait_for_readers, args=(bot.delete_message, message.chat.id, warn.id)).start()
        with shelve.open('chat_stats') as chat_stats:
            chat_stats['Banned'] += 1


def check_delete_list(type_message: types.Message) -> bool:
    """ Check for unwanted text in message and delete. """
    unwanted_phrases = ['t.me']
    for phrase in unwanted_phrases:
        if phrase in type_message.text.casefold():
            return True
        if type_message.entities:
            for entity in type_message.entities:
                if entity.url and phrase in entity.url:
                    return True


@bot.message_handler(func=check_delete_list, content_types=['text'])
def delete_message(message: types.Message):
    """ Delete unwanted message. """
    bot.delete_message(message.chat.id, message.id)
    if message.chat.id == PYTHONCHATRU:
        with shelve.open('chat_stats') as chat_stats:
            chat_stats['Deleted'] += 1


@bot.message_handler(commands=['rules'])
def send_lutz_command(message):
    """ Send Chat Rules link. """
    bot.reply_to(message,
                 '<b>🟡 <u><a href="https://telegra.ph/pythonchatru-07-07">Правила чата</a></u></b>',
                 parse_mode='HTML',
                 disable_notification=True,
                 )
    logging(message)


@bot.message_handler(commands=['faq'])
def send_lutz_command(message):
    """ Send Chat FAQ link. """
    bot.reply_to(message,
                 '<b>🔵 <u><a href="https://telegra.ph/faq-10-07-4">FAQ</a></u></b>',
                 parse_mode='HTML',
                 disable_notification=True,
                 )
    logging(message)


@bot.message_handler(commands=['lutz'])
def send_lutz_command(message):
    """ Send the Lutz's Book. """
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
    """ Send Chat's Library link. """
    bot.reply_to(message,
                 '📚 <b><u><a href="https://telegra.ph/what-to-read-10-06">Библиотека питониста</a></u></b>',
                 parse_mode='HTML',
                 disable_notification=True,
                 )
    logging(message)


@bot.message_handler(commands=['log'])
def send_log(message):
    """ Send the last log rows. """
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
    """ Inline the Zen of Python. """
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
    """ Send info about user and chat id [Service]. """
    bot.send_message(message.chat.id, get_me(message), parse_mode='HTML')
    logging(message)


@bot.message_handler(commands=['remind'])
def remind_manually(message):
    """ Remind holidays manually. """
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
    """ List all the jobs in schedule. """
    if message.chat.id == ADMIN_ID:
        bot.send_message(ADMIN_ID, reminder.print_get_jobs(),
                         parse_mode='HTML', disable_web_page_preview=True)


@bot.message_handler(commands=['stats'])
def send_stats(message):
    bot.send_message(message.chat.id, report.create_report_text(),
                     parse_mode='HTML', disable_web_page_preview=True)


@bot.message_handler(commands=['reset_stats'])
def send_stats(message):
    report.reset_report_stats()
    bot.send_message(message.chat.id, report.reset_report_stats(),
                     parse_mode='HTML', disable_web_page_preview=True)


def check_unwanted_list(type_message: types.Message) -> bool:
    """ Check for mentioning unwanted persons in text. """
    unwanted_phrases = ['дудар', 'хауди', 'howdy', 'dudar']
    for phrase in unwanted_phrases:
        if phrase in type_message.text.casefold():
            return True


@bot.message_handler(func=check_unwanted_list, content_types=['text'])
def unwanted_mentions(message: types.Message):
    """ Reply to unwanted mentions. """
    bot.reply_to(message, f'У нас таких не любят! 🥴', parse_mode='HTML')


def check_chat(message: types.Message):
    if message.chat.id == PYTHONCHATRU:
        return True


@bot.message_handler(func=check_chat, content_types=['text', 'sticker', 'photo', 'animation', 'video',
                                                     'audio', 'document'])
def unwanted_mentions(message: types.Message):
    """ Count messages. """
    with shelve.open('chat_stats', writeback=True) as s:
        s['Messages'][message.from_user.id] = s['Messages'].get(message.from_user.id,
                                                                {'Name': message.from_user.first_name,
                                                                 'Username': message.from_user.username,
                                                                 'Count': 0})
        s['Messages'][message.from_user.id]['Count'] += 1


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
