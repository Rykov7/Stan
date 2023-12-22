""" Send User's info. """
import logging
import shelve
from pathlib import Path
from urllib import parse
from urllib.request import urlopen

from telebot import types

from .constants import DATA
from .report import reset_report_stats


def my_ip():
    ip_service = "https://icanhazip.com"
    ip = urlopen(ip_service)
    return ip.read().decode("utf-8")


def me(message: types.Message):
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


def represent_as_get(message: types.Message):
    return parse.quote_plus(detect_args(message))


def detect_args(message: types.Message):
    if message.reply_to_message and message.reply_to_message.text:
        if len(message.text.split()) == 1:
            return message.reply_to_message.text
        else:
            return " ".join(message.text.split()[1:])
    else:
        if len(message.text.split()) > 1:
            return " ".join(message.text.split()[1:])


def update_stats(message: types.Message):
    if not Path(f"{DATA}{message.chat.id}").exists():
        reset_report_stats(message.chat.id)
    with shelve.open(f"{DATA}{message.chat.id}", writeback=True) as shelve_db:
        if "Messages" not in shelve_db:
            reset_report_stats(message.chat.id)
        if message.from_user.id not in shelve_db["Messages"]:
            shelve_db["Messages"][message.from_user.id] = {"User": message.from_user, "Count": 1}
            logging.info(f"[{message.chat.title[:10]}] [{message.from_user.id}] {message.from_user.first_name}")
        else:
            shelve_db["Messages"][message.from_user.id]["Count"] += 1
