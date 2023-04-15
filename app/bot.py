import shelve
from flask import request, abort

from . import stan
from . import rules

from .helpers import represent_as_get, detect_args, update_stats
from .filters import *
from .config import *

"""                [ ANTISPAM ]             """


@bot.edited_message_handler(func=in_spam_list, chat_types=["supergroup", "group"])
@bot.message_handler(func=in_spam_list, chat_types=["supergroup", "group"])
def moderate_messages(message: types.Message):
    """Ban user and delete their message."""
    bot.delete_message(message.chat.id, message.id)
    bot.ban_chat_member(message.chat.id, message.from_user.id)
    with shelve.open(f"{DATA}{message.chat.id}") as s:
        s["Banned"] += 1


@bot.message_handler(func=in_caption_spam_list, content_types=["video"], chat_types=["supergroup", "group"])
def catch_videos(message: types.Message):
    """Catch offensive videos"""
    bot.delete_message(message.chat.id, message.id)
    bot.ban_chat_member(message.chat.id, message.from_user.id)
    with shelve.open(f"{DATA}{message.chat.id}") as s:
        s["Banned"] += 1


@bot.edited_message_handler(func=in_delete_list, chat_types=["supergroup", "group"])
@bot.message_handler(func=in_delete_list, chat_types=["supergroup", "group"])
def delete_message(message: types.Message):
    """Delete unwanted message."""
    bot.delete_message(message.chat.id, message.id)
    with shelve.open(f"{DATA}{message.chat.id}") as s:
        s["Deleted"] += 1


"""                [ COMMANDS ]             """


@bot.message_handler(commands=["start", "links", "ссылки"])
def start(message: types.Message):
    """What to begin with."""
    logging.info(LOG_COMM % (message.chat.title, message.from_user.id, message.from_user.first_name, message.text))
    markup = types.InlineKeyboardMarkup([[RULES], [FAQ], [LIB]], 1)
    send_or_reply(message, "Начни с прочтения", reply_markup=markup)


@bot.message_handler(commands=["rules", "rule", "r", "правила", "правило", "п"])
def send_rules(message: types.Message):
    markup = types.InlineKeyboardMarkup([[RULES]], 1)
    args = message.text.split()
    logging.info(LOG_TEXT % (message.chat.title, message.from_user.id, message.from_user.first_name, message.text))
    if len(args) > 1 and args[-1].isdigit() and 0 < int(args[-1]):
        send_or_reply(
            message,
            f"<b>Правило {args[-1]}</b>\n<i>{rules.fetch_rule(args[-1])}</i>",
            reply_markup=markup,
        )
    else:
        send_or_reply(message, "...", reply_markup=markup)


@bot.message_handler(commands=["faq", "чзв"])
def send_faq(message: types.Message):
    logging.info(
        LOG_COMM
        % (
            message.chat.title,
            message.from_user.id,
            message.from_user.first_name,
            message.text,
        )
    )
    markup = types.InlineKeyboardMarkup([[FAQ]], 1)
    send_or_reply(message, "...", reply_markup=markup)


@bot.message_handler(commands=["lib", "library", "books", "книги", "библиотека"])
def send_lib(message: types.Message):
    logging.info(
        LOG_COMM
        % (
            message.chat.title,
            message.from_user.id,
            message.from_user.first_name,
            message.text,
        )
    )
    markup = types.InlineKeyboardMarkup([[LIB]], 1)
    send_or_reply(message, "...", reply_markup=markup)


@bot.message_handler(commands=["lutz", "лутц"])
def send_lutz(message: types.Message):
    logging.info(
        LOG_COMM
        % (
            message.chat.title,
            message.from_user.id,
            message.from_user.first_name,
            message.text,
        )
    )
    bot.send_document(
        message.chat.id,
        document="BQACAgQAAxkBAAPBYsWJG9Ml0fPrnbU9UyzTQiQSuHkAAjkDAAIstCxSkuRbXAlcqeQpBA",
        caption="вот, не позорься",
    )


@bot.message_handler(commands=["bdmtss", "бдмтсс"])
def send_bdmtss_audio(message: types.Message):
    logging.info(
        LOG_COMM
        % (
            message.chat.title,
            message.from_user.id,
            message.from_user.first_name,
            message.text,
        )
    )
    bot.send_voice(
        message.chat.id,
        "AwACAgIAAxkBAAIJrWOg2WUvLwrf7ahyJxQHB8_nqllwAAL5JQAC2_IJSbhfQIO5YnVmLAQ",
    )


@bot.message_handler(commands=["tr", "тр"])
def translate_layout(message: types.Message):
    logging.info(
        LOG_COMM
        % (
            message.chat.title,
            message.from_user.id,
            message.from_user.first_name,
            message.text,
        )
    )
    if message.reply_to_message and message.reply_to_message.text:
        if message.reply_to_message.text[0] in RUS:
            bot.send_message(
                message.chat.id, message.reply_to_message.text.translate(RUS_ENG_TABLE)
            )
        else:
            bot.send_message(
                message.chat.id, message.reply_to_message.text.translate(ENG_RUS_TABLE)
            )


@bot.message_handler(commands=["quote", "цитата"])
def stan_speak(message: types.Message):
    logging.info(
        LOG_COMM
        % (
            message.chat.title,
            message.from_user.id,
            message.from_user.first_name,
            message.text,
        )
    )
    bot.send_message(message.chat.id, stan.speak(0, message.chat.id))


@bot.message_handler(commands=["tsya", "тся", "ться"])
def send_tsya(message: types.Message):
    logging.info(
        LOG_COMM
        % (
            message.chat.title,
            message.from_user.id,
            message.from_user.first_name,
            message.text,
        )
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🧑🏼‍🎓 Читать правило", url="https://tsya.ru/"),
        row_width=1,
    )
    send_or_reply(message, "<i>-тся</i> и <i>-ться</i> в глаголах", reply_markup=markup)


@bot.message_handler(commands=["nometa", "номета"])
def send_nometa(message: types.Message):
    logging.info(
        LOG_COMM
        % (
            message.chat.title,
            message.from_user.id,
            message.from_user.first_name,
            message.text,
        )
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("❓ nometa.xyz", url="https://nometa.xyz/ru.html"),
        row_width=1,
    )
    send_or_reply(
        message,
        """Не задавай мета-вопросов вроде:
<i>  «Можно задать вопрос?»
  «Кто-нибудь пользовался .. ?»
  «Привет, мне нужна помощь по .. !»</i>

Просто спроси сразу! И чем лучше объяснишь проблему, тем вероятнее получишь помощь.""",
        reply_markup=markup,
    )


@bot.message_handler(commands=["neprivet", "непривет"])
def send_neprivet(message: types.Message):
    logging.info(
        LOG_COMM
        % (
            message.chat.title,
            message.from_user.id,
            message.from_user.first_name,
            message.text,
        )
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("👋 Непривет", url="https://neprivet.com/"),
        row_width=1,
    )
    send_or_reply(
        message, "Пожалуйста, не пишите просто «Привет» в чате.", reply_markup=markup
    )


@bot.message_handler(commands=["nojob", "ноджоб"])
def send_nojob(message):
    answer = """Мы здесь не для того, чтобы за тебя решать задачи.

Здесь помогают по конкретным вопросам в <u>ТВОЁМ</u> коде, поэтому тебе нужно показать код, который ты написал сам и \
объяснить где и почему застрял... всё просто. 🤷🏼️"""
    send_or_reply(message, answer)


@bot.message_handler(commands=["nobot", "нобот"])
def nobot(message: types.Message):
    answer = """<b>Внимание</b>:
Телеграм бот <i>не должен</i> быть твоим первым проектом на Python. Пожалуйста, изучи <code>основы Python</code>, \
<code>работу с модулями</code>, <code>основы веб-технологий</code>, <code>асинхронное программирование</code> и \
<code>отладку</code> до начала работы с Телеграм ботами. Существует много ресурсов для этого в интернете."""
    send_or_reply(message, answer)


@bot.message_handler(commands=["nogui", "ногуи"])
def nogui(message: types.Message):
    answer = """<b>Внимание</b>:
GUI приложение <i>не должно</i> быть твоим первым проектом на Python. Пожалуйста, изучи <code>основы Python</code>, \
<code>работу с модулями</code>, <code>циклы событий</code> и <code>отладку</code> до начала работы с какими-либо \
GUI-фреймворками. Существует много ресурсов для этого в интернете."""
    send_or_reply(message, answer)


@bot.message_handler(commands=["g", "г"])
def google_it(message: types.Message):
    """Google it!"""
    logging.info(
        LOG_COMM
        % (
            message.chat.title,
            message.from_user.id,
            message.from_user.first_name,
            message.text,
        )
    )
    query = f"<i>{detect_args(message)}</i>"
    get_query = "https://www.google.com/search?q=" + represent_as_get(message)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔍 Google Поиск", url=get_query), row_width=1)
    send_or_reply(message, f"<i>Ищем «{query}»...</i>", reply_markup=markup)


"""                [ ADMIN PANEL ]              """


@bot.message_handler(func=is_admin, commands=["ddel"])
def delete_user(message: types.Message):
    if message.reply_to_message:
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.reply_to_message.id)
        logging.info(
            "!DEL! (M)"
            + LOG_COMM
            % (
                message.chat.title,
                message.reply_to_message.from_user.id,
                message.from_user.first_name,
                message.reply_to_message.text,
            )
        )


@bot.message_handler(func=is_admin, commands=["bban"])
def ban_user(message: types.Message):
    if message.reply_to_message:
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.reply_to_message.id)
        bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        logging.info(
            f"!BAN! (M)"
            + LOG_COMM
            % (
                message.chat.title,
                message.reply_to_message.from_user.id,
                message.from_user.first_name,
                message.reply_to_message.text,
            )
        )


@bot.message_handler(func=is_admin, commands=["unban_id"])
def unban_user(message: types.Message):
    if message.text.split()[-1].isdigit():
        user_id = int(message.text.split()[-1])
        bot.unban_chat_member(PYTHONCHATRU, user_id)
        logging.info(f"!UNBAN (M)! {user_id}")


"""                [ INLINE ]               """


@bot.inline_handler(lambda query: True)
def default_query(inline_query):
    """Inline the Zen of Python."""
    zen = []
    for id_p, phrase in enumerate(ZEN):
        q = inline_query.query.casefold()
        if phrase.casefold().startswith(q) or " " + q in phrase.casefold():
            zen.append(
                types.InlineQueryResultArticle(
                    f"{id_p}",
                    f"The Zen of Python #{id_p + 1}",
                    types.InputTextMessageContent(f"{phrase}"),
                    description=phrase,
                )
            )

    bot.answer_inline_query(inline_query.id, zen, cache_time=1200)


"""                [ COUNTER ]              """


@bot.message_handler(
    content_types=[
        "text",
        "sticker",
        "photo",
        "animation",
        "video",
        "audio",
        "document",
    ],
    chat_types=["supergroup", "group"],
)
def handle_msg(message: types.Message):
    """Count messages, Stan."""
    update_stats(message)
    stan.act(message)


"""                [ WEBHOOK ]              """


@app.route(f"/bot{TOKEN}/", methods=["POST"])
def webhook():
    """Parse POST requests from Telegram."""
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ""
    else:
        abort(403)
