import schedule
import time
from threading import Thread
from datetime import datetime as dt
from config import bot
import csv
from dotenv import load_dotenv

from config import PYTHONCHATRU

# https://core.telegram.org/bots/api Telegram Bot API

dotenv_path = '.env'
load_dotenv(dotenv_path)


def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(20)


def remind():
    """ Remind holiday. """
    with open('holidays.csv', newline='', encoding='utf-8') as holidays_file:
        holidays = tuple(csv.reader(holidays_file))
    today = dt.today()
    for entry in holidays[1:]:
        date, holiday, description = entry
        if today.month == dt.strptime(date, "%Y-%m-%d").month and today.day == dt.strptime(date, "%Y-%m-%d").day:
            notification = f'🎉💻 Сегодня {dt.strptime(date, "%m-%d"):%d.%m}, <b><u>{holiday.upper()}</u></b>! \
                                    \n\n{description}.'
            if dt.strptime(date, "%Y-%m-%d").year != 1:
                age = today.year - dt.strptime(date, "%Y-%m-%d").year
                notification += f'\n<i>{age} годовщина</i>'
            bot.send_message(PYTHONCHATRU, notification, parse_mode='HTML')  # PYTHONCHATRU


schedule.every().day.at('07:00').do(remind)
Thread(target=scheduler).start()
