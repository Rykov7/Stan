""" Send User's info. """
from urllib import parse
from .config import bot


def get_me(message):
    msg = f"<b>Telegram ID:</b> <code>{message.from_user.id}</code>\n\
    ├ <b>Is bot:</b> {message.from_user.is_bot}\n\
    ├ <b>First name:</b> {message.from_user.first_name}\n"
    if message.from_user.last_name:
        msg += f"    ├ <b>Last name:</b> {message.from_user.last_name}\n"
    if message.from_user.username:
        msg += f"    ├ <b>Username:</b> {message.from_user.username}\n"
    msg += f"    ├ <b>Language code:</b> {message.from_user.language_code}\n"
    if message.from_user.is_premium is True:
        msg += f"    ├ <b>Is Premium</b>: ⭐️\n"
    else:
        msg += f"    ├ <b>Is Premium</b>: No\n"
    msg += f"    ├ <b>Chat ID:</b> {message.chat.id}"

    return msg


def search_it(engine, message):
    if message.reply_to_message and message.reply_to_message.text:
        if len(message.text.split()) == 1:
            r = parse.quote_plus(message.reply_to_message.text)
        else:
            r = parse.quote_plus(' '.join(message.text.split()[1:]))
        bot.reply_to(message.reply_to_message, f"{engine}{r}",
                     disable_web_page_preview=True)
    else:
        if len(message.text.split()) > 1:
            r = parse.quote_plus(' '.join(message.text.split()[1:]))
            bot.reply_to(message, f"{engine}{r}")
