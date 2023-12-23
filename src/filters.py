import logging.handlers

from telebot import types

from .config import WHITEIDS
from .constants import LOG_COMM, ALLOWED_WORDS, URL_RX
from .helpers import is_spam, is_in_not_allowed, is_ban_words_in_caption
from .models import is_antispam_enabled


def in_spam_list(message: types.Message) -> bool:
    antispam_is_enabled = is_antispam_enabled(message.chat.id)
    from_user_id, title, from_user_name = message.from_user.id, message.chat.title, message.from_user.first_name
    if from_user_id not in WHITEIDS and antispam_is_enabled:
        if is_spam(message.text):
            logging.info("!BAN!" + LOG_COMM % (title, from_user_id, from_user_name, message.text))
            return True
    return False


def in_caption_spam_list(message: types.Message) -> bool:
    """Check for mentioning unwanted words in caption."""
    if message.caption and is_ban_words_in_caption(message.caption):
        from_user_id, title, from_user_name = message.from_user.id, message.chat.title, message.from_user.first_name
        logging.info("!BAN!" + LOG_COMM % (title, from_user_id, from_user_name, message.video.file_name))
        return True
    return False


def in_delete_list(message: types.Message) -> bool:
    """Check for URLs in message and delete."""
    antispam_is_enabled = is_antispam_enabled(message.chat.id)
    from_user_id, title, from_user_name = message.from_user.id, message.chat.title, message.from_user.first_name
    if from_user_id not in WHITEIDS and antispam_is_enabled:
        if URL_RX.search(message.text) and is_in_not_allowed(ALLOWED_WORDS, message.text):
            logging.info(f"[DELETE] [{title}] [{from_user_id}] {from_user_name}: {message.text}")
            return True
        if message.entities:
            for entity in message.entities:
                if entity.url and is_in_not_allowed(ALLOWED_WORDS, entity.url):
                    logging.info(f"[DELETE] [{title}] [{from_user_id}] {from_user_name}: [entity] {message.text}")
                    return True
    return False


def is_white_id(message: types.Message) -> bool:
    return message.from_user.id in WHITEIDS
