from telebot import types
from .config import *


def check_spam_list(type_message: types.Message) -> bool:
    """ Check for mentioning unwanted persons in text. """
    if type_message.from_user.username not in WHITEUN and type_message.from_user.id not in WHITEIDS:
        for url in SPAM:
            if url in type_message.text.casefold():
                return True


def check_caption_spam_list(type_message: types.Message) -> bool:
    """ Check for mentioning unwanted words in caption. """
    for phrase in BAN_WORDS:
        if type_message.caption and phrase in type_message.caption:
            return True


def check_no_allowed(word_list, msg):
    for word in word_list:
        if word in msg.casefold():
            return False
    return True


def check_delete_list(type_message: types.Message) -> bool:
    """ Check for URLs in message and delete. """
    if type_message.from_user.username not in WHITEUN and type_message.from_user.id not in WHITEIDS:
        if URL_RX.search(type_message.text) and check_no_allowed(ALLOWED_WORDS, type_message.text):
            logging.info(f'[DEL] {type_message.from_user.id} {type_message.from_user.first_name} - {type_message.text}')
            return True
        if type_message.entities:
            for entity in type_message.entities:
                if entity.url and check_no_allowed(ALLOWED_WORDS, entity.url):
                    logging.info(
                        f'[DEL] {type_message.from_user.id} {type_message.from_user.first_name} - Entity ({entity.url})')
                    return True


def check_nongrata(type_message: types.Message) -> bool:
    """ Check for non grata persons. """
    for phrase in NON_GRATA:
        if phrase in type_message.text.casefold():
            return True


def check_chat(message: types.Message):
    if message.chat.id == PYTHONCHATRU:
        return True


def send_or_reply(m: types.Message, answer):
    if m.reply_to_message:
        bot.reply_to(m.reply_to_message, answer)
    else:
        bot.send_message(m.chat.id, answer)
