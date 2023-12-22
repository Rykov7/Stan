import asyncio

from src.webhook import app, bot

if __name__ == '__main__':
    asyncio.run(bot.infinity_polling())
