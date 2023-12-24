""" Send User's info. """

from urllib import parse
from urllib.error import URLError
from urllib.request import urlopen

from telebot import types

from .constants import SPAM, BAN_WORDS, NON_GRATA, ADMIN_ID, ONLY_RUS_LETTERS, RUS_LETTERS_AND_PUNCTUATION


def is_url_reachable(url: str) -> bool:
    try:
        return urlopen(url).status == 200
    except URLError:
        return False


def is_spam(message_text: str) -> bool:
    """
    Проверяет текст на спам - сначала проверка смешанного алфавита, потом на константный набор спам-слов
    """
    if is_mixed(message_text):
        return True
    return any(text.casefold() in message_text.casefold() for text in SPAM)


def is_mixed(text: str) -> bool:
    """
    Разбивает текст на слова и проверяет на смешанный алфавит, спамеры используют его. Слово допускается только
    полностью на русском или русский + знаки пунктуации
    """
    for word in text.split():
        word = word.strip().lower()
        if any(e in ONLY_RUS_LETTERS for e in word) and not all(e in RUS_LETTERS_AND_PUNCTUATION for e in word):
            return True
    return False


def is_in_not_allowed(word_list: list, msg: str) -> bool:
    for word in word_list:
        if word in msg.casefold():
            return False
    return True


def is_ban_words_in_caption(caption: str) -> bool:
    return any(ban_word in caption for ban_word in BAN_WORDS)


def is_nongrata(type_message: types.Message) -> bool:
    for phrase in NON_GRATA:
        if phrase in type_message.text.casefold():
            return True
    return False


def is_admin(message: types.Message) -> bool:
    return message.from_user.id == ADMIN_ID


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


def short_user_data(from_user: types.User) -> dict:
    info = {'first_name': from_user.first_name, 'last_name': from_user.last_name, 'username': from_user.username,
            'full_name': from_user.full_name, 'id': from_user.id, 'code': from_user.language_code,
            'is_bot': from_user.is_bot, 'is_premium': from_user.is_premium}
    return info


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
