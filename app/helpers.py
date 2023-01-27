""" Send User's info. """
from urllib import parse
from telebot import types


def represent_as_get(message: types.Message):
    return parse.quote_plus(detect_args(message))


def detect_args(message: types.Message):
    if message.reply_to_message and message.reply_to_message.text:
        if len(message.text.split()) == 1:
            return message.reply_to_message.text
        else:
            return ' '.join(message.text.split()[1:])
    else:
        if len(message.text.split()) > 1:
            return ' '.join(message.text.split()[1:])
