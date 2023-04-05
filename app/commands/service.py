""" Service commands for Admin purposes. """

import logging
from datetime import datetime as dt
from ..models import Chat
from ..database import session
from ..config import bot, ADMIN_ID, types
from .. import reminder
from .. import report
from ..filters import is_admin
from .get import me, my_ip


@bot.message_handler(commands=["me"])
def command_me(message):
    """Send info about user and chat id [Service]."""
    bot.send_message(message.chat.id, me(message))


@bot.message_handler(func=is_admin, commands=["ip"])
def get_ip(message):
    bot.send_message(message.chat.id, my_ip())


@bot.message_handler(commands=["remind"])
def remind_manually(message):
    """Remind holidays manually."""
    args = message.text.split()
    if len(args) > 1:
        try:
            today = dt.strptime(args[1], "%m-%d-%Y")
        except ValueError as ve:
            bot.send_message(message.chat.id, f"Не удалось разобрать дату!\n{ve}")
        else:
            reminder.remind(message.chat.id, today)
    else:
        bot.send_message(
            message.chat.id,
            f"<b>Формат даты: MM-DD-YYYY</b>\n\n"
            f"Примеры:\n"
            f"/remind 09-12-2024\n"
            f"/remind 09-13-2022",
        )


@bot.message_handler(func=is_admin, commands=["jobs"])
def list_jobs(message):
    """List all the jobs in schedule."""
    bot.send_message(ADMIN_ID, reminder.print_get_jobs())


@bot.message_handler(func=is_admin, commands=["stats"])
def send_stats(message: types.Message):
    if len(message.text.split()) == 1:
        rep = report.create_report_text(message.chat.id)
        if rep:
            bot.send_message(message.chat.id, rep)
    else:
        bot.send_message(
            message.chat.id, report.create_report_text(message.text.split()[-1])
        )


@bot.message_handler(
    func=is_admin, commands=["reset_stats"], chat_types=["supergroup", "group"]
)
def send_stats(message: types.Message):
    logging.warning("reset_stats")
    report.reset_report_stats(message.chat.id)
    bot.send_message(message.chat.id, report.reset_report_stats(message.chat.id))


@bot.message_handler(commands=["enable_stan"], chat_types=["supergroup", "group"])
def enable_stan(message: types.Message):
    """Add group to database."""

    logging.info(
        f"[{message.chat.title}] [{message.from_user.id}] {message.from_user.username}: {message.text}"
    )
    if not session.query(Chat.id).filter(Chat.id == message.chat.id).first():
        logging.info('[TRUE] chat.id == message.chat.id')
        session.add(Chat(chat_id=message.chat.id, title=message.chat.title, antispam=1, report=0, reminder=1))
        session.commit()
        bot.send_message(message.chat.id, f"""Группа "{message.chat.title}"
Добавлена в БД

Текущие настройки:
  Антиспам: {session.query(Chat.antispam).filter(Chat.chat_id == message.chat.id).first()[0]}
  Ежедневные отчёты: {session.query(Chat.report).filter(Chat.chat_id == message.chat.id).first()[0]}
  Праздники: {session.query(Chat.reminder).filter(Chat.chat_id == message.chat.id).first()[0]}""")

@bot.message_handler(commands=["get_quotes"], chat_types=["supergroup", "group"])
def get_quotes(message: types.Message):
    logging.info('[TRUE] getting quotes...')
    quotes = session.query(Chat.quotes).filter(Chat.id == message.chat.id).all()
    bot.send_message(message.chat.id, f"{quotes}")