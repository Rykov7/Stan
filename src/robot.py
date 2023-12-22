import logging

from telebot.async_telebot import AsyncTeleBot

from .config import TOKEN

logging.warning("[START] Stan")
bot = AsyncTeleBot(
    TOKEN,
    "HTML",
    disable_web_page_preview=True,
    allow_sending_without_reply=True,
    colorful_logs=True,
)
