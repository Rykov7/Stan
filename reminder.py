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

with open('holidays.csv', newline='', encoding='utf-8') as holidays_file:
    holidays = tuple(csv.reader(holidays_file))


def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(20)


def remind():
    """ Remind holiday. """
    today = dt.today()
    for entry in holidays[1:]:
        date, holiday, description = entry
        if len(date) == 5 \
                and today.month == dt.strptime(date, "%m-%d").month \
                and today.day == dt.strptime(date, "%m-%d").day:
            notification = f'🎉💻 Сегодня {dt.strptime(date, "%m-%d"):%d.%m}, <b><u>{holiday.upper()}</u></b>! \
                                    \n\n{description}.'
            bot.send_message(PYTHONCHATRU, notification, parse_mode='HTML')  # PYTHONCHATRU
        elif len(date) == 10 \
                and today.month == dt.strptime(date, "%Y-%m-%d").month \
                and today.day == dt.strptime(date, "%Y-%m-%d").day:
            age = today.year - dt.strptime(date, "%Y-%m-%d").year
            notification = f'🎉💻 Сегодня {dt.strptime(date, "%Y-%m-%d"):%d.%m}, <b><u>{holiday.upper()}</u></b>! \
                                             \n\n{description}.\n<i>{age} годовщина</i>'
            bot.send_message(PYTHONCHATRU, notification, parse_mode='HTML')  # PYTHONCHATRU


schedule.every().day.at('08:00').do(remind)
Thread(target=scheduler).start()

