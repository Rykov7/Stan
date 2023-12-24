import logging
import logging.handlers

from telebot import types

from .admin_commands import bot
from .constants import (LOG_COMM, FAQ, LIB, RULES, RUS, RUS_ENG_TABLE, ENG_RUS_TABLE, PYTHONCHATRU, ZEN, LUTZ_ID,
                        BDMTSS_ID)
from .filters import in_spam_list, in_caption_spam_list, in_delete_list
from .helpers import represent_as_get, detect_args, is_admin, fetch_rule
from .report import update_stats, increment
from .stan import act, speak


async def send_or_reply(message: types.Message, answer, **kwargs):
    if message.reply_to_message:
        await bot.reply_to(message.reply_to_message, answer, **kwargs)
    else:
        await bot.send_message(message.chat.id, answer, **kwargs)


"""                [ ANTISPAM ]             """


@bot.edited_message_handler(func=in_spam_list, chat_types=["supergroup", "group"])
@bot.message_handler(func=in_spam_list, chat_types=["supergroup", "group"])
async def moderate_messages(message: types.Message):
    """Ban user and delete their message."""
    await bot.delete_message(message.chat.id, message.id)
    await bot.ban_chat_member(message.chat.id, message.from_user.id)
    increment(message.chat.id, banned=True)


@bot.message_handler(func=in_caption_spam_list, content_types=["video"], chat_types=["supergroup", "group"])
async def catch_videos(message: types.Message):
    """Catch offensive videos"""
    await bot.delete_message(message.chat.id, message.id)
    await bot.ban_chat_member(message.chat.id, message.from_user.id)
    increment(message.chat.id, banned=True)


@bot.edited_message_handler(func=in_delete_list, chat_types=["supergroup", "group"])
@bot.message_handler(func=in_delete_list, chat_types=["supergroup", "group"])
async def delete_message(message: types.Message):
    """Delete unwanted message."""
    await bot.delete_message(message.chat.id, message.id)
    increment(message.chat.id, banned=False)


"""                [ COMMANDS ]             """


@bot.message_handler(commands=["start", "links", "ссылки"])
async def start(message: types.Message):
    """What to begin with."""
    logging.info(LOG_COMM % (message.chat.title, message.from_user.id, message.from_user.first_name, message.text))
    markup = types.InlineKeyboardMarkup([[RULES], [FAQ], [LIB]], 1)
    await send_or_reply(message, "Начни с прочтения", reply_markup=markup)
    await bot.delete_message(message.chat.id, message.id)


@bot.message_handler(commands=["rules", "rule", "r", "правила", "правило", "п"])
async def send_rules(message: types.Message):
    markup = types.InlineKeyboardMarkup([[RULES]], 1)
    args = message.text.split()
    logging.info(LOG_COMM % (message.chat.title, message.from_user.id, message.from_user.first_name, message.text))
    if len(args) > 1 and args[-1].isdigit():
        index = int(args[-1])
        await send_or_reply(
            message,
            f"<b>Правило {args[-1]}</b>\n<i>{fetch_rule(index)}</i>",
            reply_markup=markup,
        )
    else:
        await send_or_reply(message, "Читай...", reply_markup=markup)
    await bot.delete_message(message.chat.id, message.id)


@bot.message_handler(commands=["faq", "чзв"])
async def send_faq(message: types.Message):
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
    await send_or_reply(message, "Читай...", reply_markup=markup)
    await bot.delete_message(message.chat.id, message.id)


@bot.message_handler(commands=["lib", "library", "books", "книги", "библиотека"])
async def send_lib(message: types.Message):
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
    await send_or_reply(message, "Читай...", reply_markup=markup)
    await bot.delete_message(message.chat.id, message.id)


@bot.message_handler(commands=["lutz", "лутц"])
async def send_lutz(message: types.Message):
    logging.info(
        LOG_COMM
        % (
            message.chat.title,
            message.from_user.id,
            message.from_user.first_name,
            message.text,
        )
    )
    await bot.send_document(message.chat.id, document=LUTZ_ID, caption="вот, не позорься")
    await bot.delete_message(message.chat.id, message.id)


@bot.message_handler(commands=["bdmtss", "бдмтсс"])
async def send_bdmtss_audio(message: types.Message):
    logging.info(
        LOG_COMM
        % (
            message.chat.title,
            message.from_user.id,
            message.from_user.first_name,
            message.text,
        )
    )
    await bot.send_voice(message.chat.id, BDMTSS_ID)
    await bot.delete_message(message.chat.id, message.id)


@bot.message_handler(commands=["tr", "тр"])
async def translate_layout(message: types.Message):
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
            await bot.send_message(message.chat.id, message.reply_to_message.text.translate(RUS_ENG_TABLE))
        else:
            await bot.send_message(message.chat.id, message.reply_to_message.text.translate(ENG_RUS_TABLE))


@bot.message_handler(commands=["quote", "цитата"])
async def stan_speak(message: types.Message):
    logging.info(
        LOG_COMM
        % (
            message.chat.title,
            message.from_user.id,
            message.from_user.first_name,
            message.text,
        )
    )
    await bot.send_message(message.chat.id, speak(0, message.chat.id), parse_mode='Markdown')
    await bot.delete_message(message.chat.id, message.id)


@bot.message_handler(commands=["tsya", "тся", "ться"])
async def send_tsya(message: types.Message):
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
    markup.add(types.InlineKeyboardButton("🧑🏼‍🎓 Читать правило", url="https://tsya.ru/"), row_width=1)
    await send_or_reply(message, "<i>-тся</i> и <i>-ться</i> в глаголах", reply_markup=markup)
    await bot.delete_message(message.chat.id, message.id)


@bot.message_handler(commands=["nometa", "номета"])
async def send_nometa(message: types.Message):
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
    markup.add(types.InlineKeyboardButton("❓ nometa.xyz", url="https://nometa.xyz/ru.html"), row_width=1)
    await send_or_reply(
        message,
        """Не задавай мета-вопросов вроде:
<i>  «Можно задать вопрос?»
  «Кто-нибудь пользовался .. ?»
  «Привет, мне нужна помощь по .. !»</i>

Просто спроси сразу! И чем лучше объяснишь проблему, тем вероятнее получишь помощь.""",
        reply_markup=markup,
    )
    await bot.delete_message(message.chat.id, message.id)


@bot.message_handler(commands=["neprivet", "непривет"])
async def send_neprivet(message: types.Message):
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
    markup.add(types.InlineKeyboardButton("👋 Непривет", url="https://neprivet.com/"), row_width=1)
    await send_or_reply(message, "Пожалуйста, не пишите просто «Привет» в чате.", reply_markup=markup)
    await bot.delete_message(message.chat.id, message.id)


@bot.message_handler(commands=["nojob", "ноджоб"])
async def send_nojob(message):
    answer = """Мы здесь не для того, чтобы за тебя решать задачи.

Здесь помогают по конкретным вопросам в <u>ТВОЁМ</u> коде, поэтому тебе нужно показать код, который ты написал сам и \
объяснить где и почему застрял... всё просто. 🤷🏼️"""
    await send_or_reply(message, answer)
    await bot.delete_message(message.chat.id, message.id)


@bot.message_handler(commands=["nobot", "нобот"])
async def nobot(message: types.Message):
    answer = """<b>Внимание</b>:
Телеграм бот <i>не должен</i> быть твоим первым проектом на Python. Пожалуйста, изучи <code>основы Python</code>, \
<code>работу с модулями</code>, <code>основы веб-технологий</code>, <code>асинхронное программирование</code> и \
<code>отладку</code> до начала работы с Телеграм ботами. Существует много ресурсов для этого в интернете."""
    await send_or_reply(message, answer)
    await bot.delete_message(message.chat.id, message.id)


@bot.message_handler(commands=["nogui", "ногуи"])
async def nogui(message: types.Message):
    answer = """<b>Внимание</b>:
GUI приложение <i>не должно</i> быть твоим первым проектом на Python. Пожалуйста, изучи <code>основы Python</code>, \
<code>работу с модулями</code>, <code>циклы событий</code> и <code>отладку</code> до начала работы с какими-либо \
GUI-фреймворками. Существует много ресурсов для этого в интернете."""
    await send_or_reply(message, answer)
    await bot.delete_message(message.chat.id, message.id)


@bot.message_handler(commands=["g", "г"])
async def google_it(message: types.Message):
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
    get_query = f"https://www.google.com/search?q={represent_as_get(message)}"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔍 Google Поиск", url=get_query), row_width=1)
    await send_or_reply(message, f"<i>Ищем «{query}»...</i>", reply_markup=markup)


"""                [ ADMIN PANEL ]              """


@bot.message_handler(func=is_admin, commands=["ddel"])
async def delete_user(message: types.Message):
    if message.reply_to_message:
        await bot.delete_message(message.chat.id, message.id)
        await bot.delete_message(message.chat.id, message.reply_to_message.id)
        logging.info(
            "!DEL!M "
            + LOG_COMM
            % (
                message.chat.title,
                message.reply_to_message.from_user.id,
                message.reply_to_message.from_user.first_name,
                message.reply_to_message.text,
            )
        )


@bot.message_handler(func=is_admin, commands=["bban"])
async def ban_user(message: types.Message):
    if message.reply_to_message:
        await bot.delete_message(message.chat.id, message.id)
        await bot.delete_message(message.chat.id, message.reply_to_message.id)
        await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        logging.info(
            f"!BAN!M "
            + LOG_COMM
            % (
                message.chat.title,
                message.reply_to_message.from_user.id,
                message.reply_to_message.from_user.first_name,
                message.reply_to_message.text,
            )
        )


@bot.message_handler(func=is_admin, commands=["unban_id"])
async def unban_user(message: types.Message):
    if message.text.split()[-1].isdigit():
        user_id = int(message.text.split()[-1])
        await bot.unban_chat_member(PYTHONCHATRU, user_id)
        logging.info(f"!UNBAN (M)! {user_id}")


"""                [ INLINE ]               """


@bot.inline_handler(lambda query: True)
async def default_query(inline_query):
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

    await bot.answer_inline_query(inline_query.id, zen, cache_time=1200)


"""                [ COUNTER ]              """


@bot.message_handler(content_types=["text", "sticker", "photo", "animation", "video", "audio", "document"],
                     chat_types=["supergroup", "group"])
async def handle_msg(message: types.Message):
    """Count messages, Stan."""
    update_stats(message)
    await act(message)
