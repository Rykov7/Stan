""" Stan's commands and reactions. """
import asyncio
import html
import random

from sqlalchemy import delete

from .config import bot, types
from .filters import is_white, is_nongrata
from .models import session
from .models import Quote


def speak(chance_of, group_id):
    number = random.randint(0, chance_of)
    if number == 0:
        return random.choice([i[0] for i in session.query(Quote.text).filter(Quote.chat_id == group_id).all()])


async def send_quote(after_sec, message, quote):
    """Pretend Reading, pretend Typing, send."""
    if message.text:
        await asyncio.sleep(len(message.text) * 0.13 / 4)  # Reading time is quarter of the same text writing time
    await bot.send_chat_action(message.chat.id, action="typing")
    await asyncio.sleep(after_sec)  # Typing time
    await bot.send_message(message.chat.id, html.escape(quote))


async def act(message: types.Message):
    quote = speak(50, message.chat.id)
    if quote:
        await send_quote(len(quote) * 0.13, message, quote )


@bot.message_handler(func=is_white, commands=["add"])
async def add_stan_quote(message: types.Message):
    if message.reply_to_message and message.reply_to_message.text:
        quote = message.reply_to_message.text
        if quote not in [i[0] for i in session.query(Quote.text).filter(Quote.chat_id == message.chat.id).all()]:
            session.add(Quote(chat_id=message.chat.id, text=quote.replace("\n", " ")))
            session.commit()
            await bot.send_message(message.chat.id, "✅ <b>Добавил</b>\n  └ <i>" + quote.replace("\n", " ") + "</i>",)
            await bot.delete_message(message.chat.id, message.id)
        else:
            await bot.send_message(message.chat.id, f"⛔️ <b>Не добавил</b>, есть токое\n  └ <i>{quote}</i>",)


@bot.message_handler(func=is_white, commands=["remove"])
async def remove_stan_quote(message: types.Message):
    if message.reply_to_message and message.reply_to_message.text:

        quote = message.reply_to_message.text
        already_exist = session.query(Quote.text).filter_by(text=quote, chat_id=message.chat.id).first()
        if already_exist:
            session.execute(delete(Quote).filter_by(text=quote, chat_id=message.chat.id))
            session.commit()

            await bot.send_message(message.chat.id, f"✅ <b>Удалил</b>\n  └ <i>{quote}</i>",)
            await bot.delete_message(message.chat.id, message.id)
        else:
            await bot.send_message(message.chat.id, f"⛔️ <b>Нет такого</b>\n  └ <i>{quote}</i>",)


@bot.message_handler(func=is_nongrata)
async def tease_nongrata(message: types.Message):
    """Reply to non grata mentions."""
    await bot.reply_to(message, f"у нас тут таких не любят")
