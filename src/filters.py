import logging.handlers

from telebot import types

from .config import WHITEIDS
from .constants import LOG_COMM, ALLOWED_WORDS, URL_RX, HELLO_EXAMPLES
from .helpers import is_spam, is_in_not_allowed, is_ban_words_in_caption, cleaned_text, remove_spaces, has_no_letters
from .models import is_antispam_enabled


def in_spam_list(message: types.Message) -> bool:
    antispam_is_enabled = is_antispam_enabled(message.chat.id)
    from_user_id, title, from_user_name = message.from_user.id, message.chat.title, message.from_user.first_name
    if from_user_id not in WHITEIDS and antispam_is_enabled:
        if is_spam(message.text):
            logging.info("!BAN!" + LOG_COMM % (title, from_user_id, from_user_name, message.text))
            return True
        if message.forward_from:  # Запрет репостов из других групп.
            return True
    return False


def in_caption_spam_list(message: types.Message) -> bool:
    """Check for mentioning unwanted words in caption."""
    if message.caption and is_ban_words_in_caption(message.caption):
        from_user_id, title, from_user_name = message.from_user.id, message.chat.title, message.from_user.first_name
        logging.info("!BAN CAPTION!" + LOG_COMM % (title, from_user_id, from_user_name, message.caption))
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


def is_hello_text(message: types.Message) -> bool:
    text = remove_spaces(cleaned_text(message.text))
    return any(hello == text for hello in HELLO_EXAMPLES)


def is_invalid_name(message: types.Message) -> bool:
    name = message.from_user.full_name
    if name is None or name.strip() == '':
        return True
    return has_no_letters(name)
