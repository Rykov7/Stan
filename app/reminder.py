import schedule
import time
from threading import Thread
from datetime import datetime as dt
import csv

from .config import PYTHONCHATRU, bot


# https://core.telegram.org/bots/api Telegram Bot API


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
            notification = f'🎉💻 Сегодня {dt.strptime(date, "%Y-%m-%d"):%d.%m}, <b><u>{holiday.upper()}</u></b>!\
                                    \n\n{description}.'
            if dt.strptime(date, "%Y-%m-%d").year != 1:
                age = today.year - dt.strptime(date, "%Y-%m-%d").year
                notification += f'\n<i>{age} годовщина</i>'
            bot.send_message(PYTHONCHATRU, notification, parse_mode='HTML')  # PYTHONCHATRU


def get_jobs():
    all_jobs = schedule.get_jobs()
    text = f"├ <b>Jobs:</b> {str(len(all_jobs))}\
\n├ {dt.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    text += '<i>' + str(all_jobs) + '</i>'
    return text


schedule.every().day.at('06:00').do(remind)
Thread(target=scheduler).start()
