import asyncio
import html
import logging

import requests
import telebot
from fastapi import FastAPI
from starlette.responses import HTMLResponse

from .commands import bot
from .config import TOKEN, log_buffer

logging.warning("[START] Webhook server")
app = FastAPI(docs=None, redoc_url=None)
BOT_API_URL = f"https://api.telegram.org/bot{TOKEN}/getMe"

@app.post(f"/bot{TOKEN}/")
async def webhook(update: dict):
    """Parse POST requests from Telegram."""
    if update:
        update = telebot.types.Update.de_json(update)
        asyncio.ensure_future(bot.process_new_updates([update]))
    else:
        return None


@app.get("/stan-logs", response_class=HTMLResponse)
def logs():
    body = "<br>".join(html.escape(line) for line in log_buffer)
    return f"""
    <html>
      <head>
        <meta charset="utf-8">
        <script>
          setInterval(() => location.reload(), 5000);
        </script>
        <title>Stan Logs</title>
        <style>
          body {{
            font-family: monospace;
            background: #111;
            color: #0f0;
          }}
        </style>
      </head>
      <body>{body}</body>
    </html>
    """


@app.get("/healthz")
async def healthcheck():
    """Проверка здоровья для Docker."""
    # Cам FastAPI
    result = {"status": "ok"}

    # Telegram API
    try:
        resp = requests.get(BOT_API_URL)
        if resp.status_code != 200:
            result["telegram_api"] = f"error {resp.status_code}"
        else:
            result["telegram_api"] = "ok"
    except Exception as e:
        result["telegram_api"] = str(e)

    return result
