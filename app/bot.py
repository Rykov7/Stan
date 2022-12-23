import shelve
from datetime import datetime as dt
from flask import Flask, request, abort
from urllib import parse
import threading
from time import sleep

from . import stan
from . import reminder
from . import reloader
from . import report
from .me import get_me
from .filters import *
from .config import *

app = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    """ Just write log. Nothing happen. """
    log_msg = f'[START] {message.from_user.id} {message.from_user.first_name}'
    if message.from_user.last_name:
        log_msg += f' {message.from_user.last_name}'
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}\nЗдесь можно опробовать команды из меню.')
    logging.warning(log_msg)


"""
            [ ANTISPAM FILTERS ]
"""


@bot.edited_message_handler(func=check_spam_list)
@bot.message_handler(func=check_spam_list)
def moderate_messages(message: types.Message):
    """ Ban user and delete their message. """
    logging.warning(f'[BAN] {message.from_user.id} {message.from_user.username} - {message.text}')
    bot.delete_message(message.chat.id, message.id)
    bot.ban_chat_member(message.chat.id, message.from_user.id)
    with shelve.open(f'{DATA}{message.chat.id}') as s:
        s['Banned'] += 1


@bot.message_handler(func=check_caption_spam_list, content_types=['video'])
def catch_videos(message: types.Message):
    """Catch offensive videos"""
    logging.warning(f'[BAN] {message.from_user.id} {message.from_user.first_name} - {message.video.file_name}')
    bot.delete_message(message.chat.id, message.id)
    bot.ban_chat_member(message.chat.id, message.from_user.id)
    with shelve.open(f'{DATA}{message.chat.id}') as s:
        s['Banned'] += 1


@bot.edited_message_handler(func=check_delete_list)
@bot.message_handler(func=check_delete_list)
def delete_message(message: types.Message):
    """ Delete unwanted message. """
    bot.delete_message(message.chat.id, message.id)
    with shelve.open(f'{DATA}{message.chat.id}') as s:
        s['Deleted'] += 1


"""
            [ COMMANDS ]
"""


@bot.message_handler(commands=['links'])
def send_links(message):
    send_or_reply(message, f"{RULES}\n{FAQ}\n{LIB}")


@bot.message_handler(commands=['rules'])
def send_rules(message):
    send_or_reply(message, f'{RULES}')


@bot.message_handler(commands=['faq'])
def send_faq(message):
    send_or_reply(message, f'{FAQ}')


@bot.message_handler(commands=['lib', 'library', 'books'])
def send_lib(message):
    send_or_reply(message, f'{LIB}')


@bot.message_handler(commands=['lutz'])
def send_lutz(message):
    bot.send_document(message.chat.id,
                      document='BQACAgQAAxkBAAPBYsWJG9Ml0fPrnbU9UyzTQiQSuHkAAjkDAAIstCxSkuRbXAlcqeQpBA',
                      caption="вот, не позорься")


@bot.message_handler(commands=['bdmtss'])
def send_bdmtss_audio(message):
    bot.send_voice(message.chat.id, 'AwACAgIAAxkBAAIJrWOg2WUvLwrf7ahyJxQHB8_nqllwAAL5JQAC2_IJSbhfQIO5YnVmLAQ')


@bot.message_handler(commands=['tr'])
def translate_layout(message):
    if message.reply_to_message and message.reply_to_message.text:
        if message.reply_to_message.text[0] in RUS:
            bot.send_message(message.chat.id, message.reply_to_message.text.translate(RUS_ENG_TABLE))
        else:
            bot.send_message(message.chat.id, message.reply_to_message.text.translate(ENG_RUS_TABLE))


@bot.message_handler(commands=['me'])
def command_me(message):
    """ Send info about user and chat id [Service]. """
    bot.send_message(message.chat.id, get_me(message))


@bot.message_handler(commands=['remind'])
def remind_manually(message):
    """ Remind holidays manually. """
    args = message.text.split()
    if len(args) > 1:
        try:
            today = dt.strptime(args[1], "%m-%d-%Y")
        except ValueError as ve:
            bot.send_message(message.chat.id, f"Не удалось разобрать дату!\n{ve}")
        else:
            reminder.remind(message.chat.id, today)
    else:
        bot.send_message(message.chat.id, f"<b>Формат даты: MM-DD-YYYY</b>\n\n"
                                          f"Примеры:\n"
                                          f"/remind 09-12-2024\n"
                                          f"/remind 09-13-2022")


@bot.message_handler(commands=['quote'])
def stan_speak(message):
    bot.send_message(message.chat.id, stan.speak(0))


@bot.message_handler(commands=['tsya'])
def send_tsya(message: types.Message):
    send_or_reply(message, '<a href="https://tsya.ru/">-тся/-ться</a>')


@bot.message_handler(commands=['nometa'])
def send_nometa(message: types.Message):
    send_or_reply(message, """Не задавай мета-вопросов, вроде:
<i>  «Можно задать вопрос?»
  «Кто-нибудь пользовался .. ?»
  «Привет, мне нужна помощь по .. !»</i>

Просто спроси сразу! И чем лучше объяснишь проблему, тем вероятнее получишь помощь.
<i><a href="https://nometa.xyz/ru.html">nometa.xyz</a></i>""")


@bot.message_handler(commands=['neprivet'])
def send_neprivet(message: types.Message):
    send_or_reply(message, '<a href="https://neprivet.com/">Непривет</a>')


@bot.message_handler(commands=['nojob'])
def send_nojob(message):
    logging.warning('Sent no job')
    answer = """Мы здесь не для того, чтобы за тебя решать задачи.

Здесь помогают по конкретным вопросам в <u>ТВОЁМ</u> коде, поэтому тебе нужно показать код, который ты написал сам и объяснить где и почему застрял... всё просто. 🤷🏼️"""
    send_or_reply(message, answer)


@bot.message_handler(commands=['nobot'])
def nobot(message: types.Message):
    answer = """<b>Внимание</b>:
Телеграм бот <i>не должен</i> быть твоим первым проектом на Python. Пожалуйста, изучи <code>основы Python</code>, <code>работу с модулями</code>, <code>основы веб-технологий</code>, <code>асинхронное программирование</code> и <code>отладку</code> до начала работы с Телеграм ботами. Существует много ресурсов для этого в интернете."""
    send_or_reply(message, answer)


@bot.message_handler(commands=['nogui'])
def nogui(message: types.Message):
    answer = """<b>Внимание</b>:
GUI приложение <i>не должно</i> быть твоим первым проектом на Python. Пожалуйста, изучи <code>основы Python</code>, <code>работу с модулями</code>, <code>циклы событий</code> и <code>отладку</code> до начала работы с какими-либо GUI-фреймворками. Существует много ресурсов для этого в интернете."""
    send_or_reply(message, answer)


@bot.message_handler(commands=['g'])
def google_it(message: types.Message):
    """ Google it! """
    search_engine = 'https://www.google.com/search?q='
    if message.reply_to_message and message.reply_to_message.text:
        if len(message.text.split()) == 1:
            r = parse.quote_plus(message.reply_to_message.text)
        else:
            r = parse.quote_plus(' '.join(message.text.split()[1:]))
        bot.reply_to(message.reply_to_message, f"{search_engine}{r}",
                     disable_web_page_preview=True)
    else:
        if len(message.text.split()) > 1:
            r = parse.quote_plus(' '.join(message.text.split()[1:]))
            bot.reply_to(message, f"{search_engine}{r}")


@bot.message_handler(func=check_nongrata)
def tease_nongrata(message: types.Message):
    """ Reply to non grata mentions. """
    bot.reply_to(message, f'у нас тут таких не любят')


"""
            [ INLINE QUERIES ]
"""


@bot.inline_handler(lambda query: True)
def default_query(inline_query):
    """ Inline the Zen of Python. """
    zen = []
    for id_p, phrase in enumerate(ZEN):
        q = inline_query.query.casefold()
        if phrase.casefold().startswith(q) or ' ' + q in phrase.casefold():
            zen.append(types.InlineQueryResultArticle(
                f"{id_p + 7000}", f'The Zen of Python #{id_p + 1}', types.InputTextMessageContent(
                    f"<i>{phrase}</i>"), description=phrase))

    bot.answer_inline_query(inline_query.id, zen, cache_time=1200)


"""
                   [ ADMIN PANEL ]
"""


@bot.message_handler(func=is_admin, commands=['reload'])
def send_stats(message):
    logging.warning('Reloading...')
    reloader.reload_modules()
    bot.send_message(message.chat.id, 'Reloaded successfully')


@bot.message_handler(func=is_admin, commands=['ddel', 'bban', 'unban_id'])
def admin_panel(message: types.Message):
    """ Admin panel. """
    if message.text == '/ddel' and message.reply_to_message:
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.reply_to_message.id)
        logging.warning(
            f'[DEL (M)] {message.reply_to_message.from_user.id} {message.reply_to_message.from_user.first_name} - {message.reply_to_message.text}')
    elif message.text == '/bban' and message.reply_to_message:
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.reply_to_message.id)
        bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        logging.warning(
            f'[BAN (M)] {message.reply_to_message.from_user.id} {message.reply_to_message.from_user.first_name} - {message.reply_to_message.text}')
    elif message.text.split()[0] == '/unban_id' and message.text.split()[-1].isdigit():
        unban_id = int(message.text.split()[-1])
        bot.unban_chat_member(PYTHONCHATRU, unban_id)
        logging.warning(f'[UNBAN (M)] {unban_id}')


@bot.message_handler(func=is_admin, commands=['jobs'])
def list_jobs(message):
    """ List all the jobs in schedule. """
    bot.send_message(ADMIN_ID, reminder.print_get_jobs())


@bot.message_handler(func=is_admin, commands=['add'])
def add_stan_quote(message):
    if message.reply_to_message and message.reply_to_message.text:
        with open('Stan.txt', 'a', encoding='utf8') as stan_quotes:
            stan_quotes.write('\n' + message.reply_to_message.text)
            bot.send_message(message.chat.id, f'Добавил: {message.reply_to_message.text}')


@bot.message_handler(func=is_admin, commands=['stats'])
def send_stats(message: types.Message):
    if len(message.text.split()) == 1:
        bot.send_message(message.chat.id, report.create_report_text(message.chat.id))
    else:
        bot.send_message(message.chat.id, report.create_report_text(message.text.split()[-1]))


@bot.message_handler(func=is_admin, commands=['reset_stats'], chat_types=['supergroup', 'group'])
def send_stats(message: types.Message):
    logging.warning('reset_stats')
    report.reset_report_stats(message.chat.id)
    bot.send_message(message.chat.id, report.reset_report_stats(message.chat.id))


"""
            [ MAIN MESSAGE HANDLER ]
"""


def send_quote(after_sec, message, quote):
    """ Imitate Reading first, then imitate Typing. """
    if message.text:
        sleep(len(message.text) * 0.13 / 4)  # Reading time is quarter of the same text writing time
    bot.send_chat_action(message.chat.id, action='typing')
    sleep(after_sec)  # Typing time
    bot.send_message(message.chat.id, quote)


@bot.message_handler(content_types=['text', 'sticker', 'photo', 'animation', 'video', 'audio', 'document'],
                     chat_types=['supergroup', 'group'])
def handle_msg(message: types.Message):
    """ Count messages, Stan. """
    with shelve.open(f'{DATA}{message.chat.id}', writeback=True) as s:
        if 'Messages' not in s:
            report.reset_report_stats(message.chat.id)

        if message.from_user.id not in s['Messages']:
            s['Messages'][message.from_user.id] = {'User': message.from_user, 'Count': 1}
            logging.warning(f'CNTR {message.chat.id}: {message.from_user.first_name} ({message.from_user.id})')
        else:
            s['Messages'][message.from_user.id]['Count'] += 1

    quote = stan.speak(25)
    if quote:
        threading.Thread(target=send_quote, args=(len(quote) * 0.13, message, quote)).start()


"""
            [ WEBHOOK ROUTE ]
"""


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
