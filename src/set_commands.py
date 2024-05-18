"""
Используется только при перезагрузке, для простоты используем синхронную версию бота.
"""

import telebot

from src.config import WHITEIDS
from src.constants import PYTHONCHATRU
from src.reminder import bot

for white_id in WHITEIDS:
    bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("nobot", "/нобот Телебот не должен быть первым проектом"),
            telebot.types.BotCommand("nogui", "/ногуи GUI приложение не должно быть первым проектом"),
            telebot.types.BotCommand("nojob", "/ноджоб, Мы здесь не для того чтобы за тебя решать задачи"),
            telebot.types.BotCommand("nometa", "/номета Не задавайте мета-вопросов"),
            telebot.types.BotCommand("neprivet", "/непривет"),
            telebot.types.BotCommand("quote", "/цитата Случайная цитата"),
            telebot.types.BotCommand("lutz", "/лутц Книга Learning Python"),
            telebot.types.BotCommand("bdmtss", "/бдмтсс Римшот"),
            telebot.types.BotCommand("g", "/г Загуглить (аргументы или цитируемое)"),
            telebot.types.BotCommand("rules", "/правила чата (работает с аргументом-номером пункта)"),
            telebot.types.BotCommand("faq", "/чзв Частые вопросы"),
            telebot.types.BotCommand("books", "/библиотека питониста"),
            telebot.types.BotCommand("links", "/ссылки на правила, чзв и библиотеку"),
            telebot.types.BotCommand("tsya", "/тся и /ться"),
            telebot.types.BotCommand("add", "добавить цитату [Whitelist]"),
            telebot.types.BotCommand("remove", "удалить цитату [Whitelist]"),
        ],
        scope=telebot.types.BotCommandScopeChatMember(PYTHONCHATRU, white_id)
    )
