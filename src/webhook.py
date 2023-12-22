import logging

import telebot
from fastapi import FastAPI

from .commands import bot
from .config import TOKEN

logging.warning("[START] Webhook server")
app = FastAPI(docs=None, redoc_url=None)


@app.post(f"/bot{TOKEN}/")
async def webhook(update: dict):
    """Parse POST requests from Telegram."""
    if update:
        update = telebot.types.Update.de_json(update)
        await bot.process_new_updates([update])
    else:
        return None
