""" Stan's commands and reactions. """
import asyncio
import html
import logging
import random
from time import time

from telebot import types

from .filters import is_white_id
from .helpers import is_nongrata, short_user_data, has_links
from .models import all_chat_quotes, add_quote, is_quote_in_chat, delete_quote_in_chat
from .robot import bot

TYPING_TIMEOUT = 0.13 / 4  # Reading time is quarter of the same text writing time
FOR_EVER_TIMEOUT = 0
ONE_DAY_TIMEOUT = 86400
ONE_WEEK_TIMEOUT = 86400 * 7


def speak(chance_of: int, chat_id: int) -> None | str:
    number = random.randint(0, chance_of)
    if number == 0:
        return random.choice(all_chat_quotes(chat_id))
    return None


async def send_quote(after_sec, message, quote):
    """Pretend Reading, pretend Typing, send."""
    if message.text:
        await asyncio.sleep(len(message.text) * TYPING_TIMEOUT)
    await bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(after_sec)  # Typing time
    await bot.send_message(message.chat.id, html.escape(quote))


async def act(message: types.Message):
    quote = speak(50, message.chat.id)
    if quote:
        await send_quote(len(quote) * 0.13, message, quote)


async def mute_forever(chat_id: int, user_id: int):
    await mute(chat_id, user_id, FOR_EVER_TIMEOUT)


async def mute_for_one_day(chat_id: int, user_id: int):
    await mute(chat_id, user_id, ONE_DAY_TIMEOUT)


async def mute_for_one_week(chat_id: int, user_id: int):
    await mute(chat_id, user_id, ONE_WEEK_TIMEOUT)


async def mute(chat_id, user_id, period):
    logging.info(f"[MUTED] User {user_id} has been muted for: {period} seconds")
    await bot.restrict_chat_member(chat_id, user_id, until_date=time() + period)


@bot.message_handler(func=is_white_id, commands=["add"])
async def add_stan_quote(message: types.Message):
    if message.reply_to_message and message.reply_to_message.text:
        quote = message.reply_to_message.text
        if not is_quote_in_chat(quote, message.chat.id):
            add_quote(message.chat.id, quote.replace("\n", " "))
            await bot.send_message(message.chat.id, "➕\n  └ " + quote.replace("\n", " "), parse_mode='Markdown')
            await bot.delete_message(message.chat.id, message.id)
        else:
            await bot.send_message(message.chat.id, f"⛔️ Не добавил, есть токое\n  └ {quote}", parse_mode='Markdown')


@bot.message_handler(func=is_white_id, commands=["remove"])
async def remove_stan_quote(message: types.Message):
    if message.reply_to_message and message.reply_to_message.text:
        quote = message.reply_to_message.text
        if is_quote_in_chat(quote, message.chat.id):
            delete_quote_in_chat(quote, message.chat.id)
            await bot.send_message(message.chat.id, f"➖ \n  └ {quote}", parse_mode='Markdown')
            await bot.delete_message(message.chat.id, message.id)
        else:
            await bot.send_message(message.chat.id, f"⛔️ Нет такого\n  └ {quote}", parse_mode='Markdown')


@bot.message_handler(func=is_nongrata)
async def tease_nongrata(message: types.Message):
    """Reply to non grata mentions."""
    await bot.reply_to(message, "у нас тут таких не любят")


@bot.message_handler(content_types=['new_chat_members', 'left_chat_member'])
async def check_new_members(message: types.Message):
    if message.content_type == "new_chat_members":
        from_user = message.from_user
        info = short_user_data(from_user)
        await bot.delete_message(message.chat.id, message.id)
        # мы не знаем как быстро получим инфу о био, потому сначала удаляем сообщение, потом запрашиваем био/логируем
        more_data = await bot.get_chat(info['id'])
        info['bio'] = more_data.bio
        if more_data.photo:
            info['photo'] = more_data.photo.big_file_id
        if info['bio'] and has_links(info['bio']):
            await bot.ban_chat_member(message.chat.id, info['id'])
            logging.info(f"[BANNED] User {info['full_name']} has url in bio: {info['bio']}")
        else:
            logging.info(f"[JOINED] {info['full_name']}")
    if message.content_type == "left_chat_member":
        from_user = message.from_user
        info = short_user_data(from_user)
        logging.info(f"[LEFT] {info['full_name']}")
        await bot.delete_message(message.chat.id, message.id)
