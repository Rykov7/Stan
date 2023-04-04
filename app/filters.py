from .config import *


def in_spam_list(message: types.Message) -> bool:
    """Check for mentioning unwanted persons in text."""
    if message.from_user.id not in WHITEIDS:
        for url in SPAM:
            if url in message.text.casefold():
                return True


def in_caption_spam_list(type_message: types.Message) -> bool:
    """Check for mentioning unwanted words in caption."""
    for phrase in BAN_WORDS:
        if type_message.caption and phrase in type_message.caption:
            return True


def in_not_allowed(word_list, msg):
    for word in word_list:
        if word in msg.casefold():
            return False
    return True


def in_delete_list(message: types.Message) -> bool:
    """Check for URLs in message and delete."""
    if message.from_user.id not in WHITEIDS:
        if URL_RX.search(message.text) and in_not_allowed(
            ALLOWED_WORDS, message.text
        ):
            logging.info(
                f"[DELETE] [{message.chat.id}] [{message.from_user.id}] {message.from_user.first_name}: {message.text}"
            )
            return True
        if message.entities:
            for entity in message.entities:
                if entity.url and in_not_allowed(ALLOWED_WORDS, entity.url):
                    logging.info(
                        f"[DELETE] [{message.chat.id}] [{message.from_user.id}] {message.from_user.first_name}: (entity) {entity.url}"
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
