from .models import session
from .models import Chat
from .config import *


def in_spam_list(message: types.Message) -> bool:
    """Check for mentioning unwanted persons in text."""
    antispam_is_enabled = session.query(Chat.antispam).filter_by(chat_id=message.chat.id).first()[0]
    if message.from_user.id not in WHITEIDS and antispam_is_enabled:
        for text in SPAM:
            if text in message.text.casefold():
                logging.info(
                    "!BAN!" + LOG_COMM % (
                    message.chat.title, message.from_user.id, message.from_user.first_name, message.text))
                return True


def in_caption_spam_list(message: types.Message) -> bool:
    """Check for mentioning unwanted words in caption."""
    for phrase in BAN_WORDS:
        if message.caption and phrase in message.caption:
            logging.info("!BAN!" + LOG_COMM % (
                message.chat.title, message.from_user.id, message.from_user.first_name, message.video.file_name))
            return True


def in_not_allowed(word_list, msg):
    for word in word_list:
        if word in msg.casefold():
            return False
    return True


def in_delete_list(message: types.Message) -> bool:
    """Check for URLs in message and delete."""
    antispam_is_enabled = session.query(Chat.antispam).filter_by(chat_id=message.chat.id).first()[0]
    if message.from_user.id not in WHITEIDS and antispam_is_enabled:
        if URL_RX.search(message.text) and in_not_allowed(
            ALLOWED_WORDS, message.text
        ):
            logging.info(
                f"[DELETE] [{message.chat.title}] [{message.from_user.id}] {message.from_user.first_name}: {message.text}"
            )
            return True
        if message.entities:
            for entity in message.entities:
                if entity.url and in_not_allowed(ALLOWED_WORDS, entity.url):
                    logging.info(
                        f"[DELETE] [{message.chat.title}] [{message.from_user.id}] {message.from_user.first_name}: [entity] {message.text}"
                    )
                    return True


def is_nongrata(type_message: types.Message) -> bool:
    """Check for non grata persons."""
    for phrase in NON_GRATA:
        if phrase in type_message.text.casefold():
            return True


def is_admin(message: types.Message) -> bool:
    return message.from_user.id == ADMIN_ID


def is_white(message: types.Message) -> bool:
    return message.from_user.id in WHITEIDS


def send_or_reply(m: types.Message, answer, **kwargs):
    if m.reply_to_message:
        bot.reply_to(m.reply_to_message, answer, **kwargs)
    else:
        bot.send_message(m.chat.id, answer, **kwargs)
