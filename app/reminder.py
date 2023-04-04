""" Schedule holidays. """

from schedule import repeat, every, get_jobs, run_pending
import time
from threading import Thread
from datetime import datetime as dt
import csv
from .config import PYTHONCHATRU, bot
from . import report


def scheduler():
    while True:
        run_pending()
        time.sleep(300)


@repeat(every().day.at("07:00"), PYTHONCHATRU, None)
def remind(chat_to_repeat, today):
    """Remind holiday."""
    if not today:
        today = dt.today()
    with open("holidays.csv", newline="", encoding="utf-8") as holidays_file:
        holidays = tuple(csv.reader(holidays_file))[1:]
    for entry in holidays:
        date, holiday, description = entry
        if today.year % 4 == 0 and holiday == "День программиста":
            date = "09-12-1000"  # instead of 09-13-1000 in non-leap-year
        date = dt.strptime(date, "%m-%d-%Y")
        if today.month == date.month and today.day == date.day:
            notification = f"🎉 Сегодня <b><u>{holiday.upper()}</u></b>!\
                                    \n\n{description}."
            if date.year != 1000:
                age = today.year - date.year
                notification += f"\n\n🥳 <i>{age}-ая годовщина</i>"
            bot.send_message(chat_to_repeat, notification)


@repeat(every().day.at("06:00"), PYTHONCHATRU)
def stat_report(chat_to_repeat):
    rep = report.create_report_text(PYTHONCHATRU)
    if rep:
        bot.send_message(chat_to_repeat, rep)
    report.reset_report_stats(PYTHONCHATRU)


def print_get_jobs():
    all_jobs = get_jobs()
    text = f"<b>{len(all_jobs)} jobs</b>\
\n..:: {dt.now().strftime('%d-%m-%Y %H:%M:%S')} ::..\n"
    for i in all_jobs:
        text += f"\n · {i!r}"
    return text


Thread(target=scheduler).start()
