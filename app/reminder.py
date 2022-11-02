""" Schedule holidays. """

from schedule import repeat, every, get_jobs, run_pending
import time
from threading import Thread
from datetime import datetime as dt
import csv
import shelve
from .config import PYTHONCHATRU, bot


# https://core.telegram.org/bots/api Telegram Bot API


def scheduler():
    while True:
        run_pending()
        time.sleep(300)


@repeat(every().day.at('06:00'), PYTHONCHATRU, None)
def remind(chat_to_repeat, today):
    """ Remind holiday. """
    if not today:
        today = dt.today()
    with open('holidays.csv', newline='', encoding='utf-8') as holidays_file:
        holidays = tuple(csv.reader(holidays_file))[1:]
    for entry in holidays:
        date, holiday, description = entry
        if today.year % 4 == 0 and holiday == 'День программиста':
            date = '09-12-1000'  # instead of 09-13-1000 in non-leap-year
        date = dt.strptime(date, "%m-%d-%Y")
        if today.month == date.month and today.day == date.day:
            notification = f'🎉 Сегодня <b><u>{holiday.upper()}</u></b>!\
                                    \n\n{description}.'
            if date.year != 1000:
                age = today.year - date.year
                notification += f'\n\n🥳 <i>{age}-ая годовщина</i>'
            bot.send_message(chat_to_repeat, notification, parse_mode='HTML')


@repeat(every().day.at('05:00'), PYTHONCHATRU)
def stat_report(chat_to_repeat):
    with shelve.open('chat_stats') as s:
        bot.send_message(chat_to_repeat, f"""<code>Доброе утро, мир!</code>
            
👮🏼 <b>Статистика нарушений за сутки</b>
    ├ <b>Заблокировано спамеров:</b> {s['Banned']}
    └ <b>Удалено сообщений:</b> {s['Deleted']}""", parse_mode='HTML')
        s['Banned'] = s['Deleted'] = 0  # Clear


def print_get_jobs():
    all_jobs = get_jobs()
    text = f"├ <b>Jobs:</b> {str(len(all_jobs))}\
\n├ {dt.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    text += '<i>' + str(all_jobs) + '</i>'
    return text


Thread(target=scheduler).start()
