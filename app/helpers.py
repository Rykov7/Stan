""" Send User's info. """
import shelve
import logging
from . import report
from .config import DATA
from urllib import parse
from telebot import types


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
    with shelve.open(f"{DATA}{message.chat.id}", writeback=True) as s:
        if "Messages" not in s:
            report.reset_report_stats(message.chat.id)

        if message.from_user.id not in s["Messages"]:
            s["Messages"][message.from_user.id] = {
                "User": message.from_user,
                "Count": 1,
            }
            logging.warning(
                f"CNTR {message.chat.id}: {message.from_user.first_name} ({message.from_user.id})"
            )
        else:
            s["Messages"][message.from_user.id]["Count"] += 1
