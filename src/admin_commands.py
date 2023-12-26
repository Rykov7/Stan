import logging
from datetime import datetime as dt

from telebot import types, logger

from .constants import ADMIN_ID, LOGGING_LEVEL_DEBUG, LOGGING_LEVEL_INFO
from .filters import is_white_id
from .helpers import me, my_ip, is_admin
from .models import is_chat_exists, add_chat, delete_chat, update_chat, chat_by_id, all_chat_quotes
from .reminder import remind, print_get_jobs, create_report_text
from .report import reset_report_stats, current_data
from .robot import bot


@bot.message_handler(commands=["me"])
async def send_me(message):
    """Send info about user and chat id [Service]."""
    await bot.send_message(message.chat.id, me(message))


@bot.message_handler(func=is_admin, commands=["ip"])
async def get_ip(message):
    await bot.send_message(message.chat.id, my_ip())


@bot.message_handler(commands=["remind"])
async def remind_manually(message):
    """Remind holidays manually."""
    args = message.text.split()
    if len(args) > 1:
        try:
            today = dt.strptime(args[1], "%m-%d-%Y")
        except ValueError as ve:
            await bot.send_message(message.chat.id, f"Не удалось разобрать дату!\n{ve}")
        else:
            remind(message.chat.id, today)
    else:
        await bot.send_message(
            message.chat.id,
            f"<b>Формат даты: MM-DD-YYYY</b>\n\n"
            f"Примеры:\n"
            f"/remind 09-12-2024\n"
            f"/remind 09-13-2022",
        )


@bot.message_handler(func=is_admin, commands=["jobs"])
async def list_jobs(_message):
    """List all the jobs in schedule."""
    await bot.send_message(ADMIN_ID, print_get_jobs())


@bot.message_handler(func=is_admin, commands=["stats"])
async def send_stats(message: types.Message):
    """Show group statistics."""
    chat_id = message.chat.id if len(splitted := message.text.split()) == 1 else splitted[-1]
    report_text = create_report_text(chat_id)
    if report_text:
        await bot.send_message(message.chat.id, report_text)
    else:
        shelve_messages, banned = current_data(chat_id)
        logging.info(f"[STATS {chat_id}] Невозможно отправить отчёт, недостаточно данных. "
                     f"Счётчик сообщений: {shelve_messages}.\nБаны: {banned}")


@bot.message_handler(func=is_admin, commands=["reset_stats"], chat_types=["supergroup", "group"])
async def send_stats(message: types.Message):
    logging.warning("reset_stats")
    reset_report_stats(message.chat.id)
    await bot.send_message(message.chat.id, reset_report_stats(message.chat.id))


@bot.message_handler(func=is_white_id, commands=["enable_stan"], chat_types=["supergroup", "group"])
async def enable_stan(message: types.Message):
    """Add group to database."""
    logging.info(f"[{message.chat.title}] [{message.from_user.id}] {message.from_user.username}: {message.text}")
    if not is_chat_exists(message.chat.id):
        add_chat(message.chat.id, message.chat.title)
        await bot.send_message(
            message.chat.id,
            f'Группа "{message.chat.title}" добавлена в БД.\n/get_group_info - узнать текущие настройки')
    else:
        await bot.send_message(message.chat.id, "Отказ. Группа уже включена")


@bot.message_handler(func=is_admin, commands=["disable_stan"], chat_types=["supergroup", "group"])
async def disable_stan(message: types.Message):
    logging.info(f"[{message.chat.title}] [{message.from_user.id}] {message.from_user.username}: {message.text}")
    if is_chat_exists(message.chat.id):
        title = delete_chat(message.chat.id)
        await bot.send_message(message.chat.id, f"Группа {title} и все связанные с ней цитаты удалены!")
    else:
        await bot.send_message(message.chat.id, "Отказ. Этой группы нет в БД.")


@bot.message_handler(
    func=is_white_id,
    commands=["set_antispam_report_reminder", "set_rules"],
    chat_types=["supergroup", "group"],
)
async def set_antispam_report_reminder(message: types.Message):
    args = message.text.split()
    if len(args) == 4:
        try:
            antispam = int(args[1])
            rep = int(args[2])
            rem = int(args[3])
        except ValueError:
            logging.info(f"[ERROR] Неверные аргументы {message.text}")
        else:
            update_chat(message.chat.id, antispam, rep, rem)
            await bot.send_message(message.chat.id, "Настройки обновлены. Проверить: /get_group_info")


@bot.message_handler(func=is_white_id, commands=["get_quotes"], chat_types=["supergroup", "group"])
async def get_quotes(message: types.Message):
    logging.info(f"[{message.chat.id}] {message.from_user.first_name} {message.text}.")
    quotes = all_chat_quotes(message.chat.id)
    if quotes:
        text = f"Количество цитат: {len(quotes)}\n\nПоследние добавленные:\n\n"
        text += "\n".join(f"· {quote}" for quote in quotes[-10:])
        await bot.send_message(message.chat.id, f"{text}")
    else:
        await bot.send_message(message.chat.id, "Цитаты отсутствуют. Подробнее: /get_group_info")


@bot.message_handler(func=is_white_id, commands=["get_group_info"], chat_types=["supergroup", "group"])
async def get_group_info(message: types.Message):
    group = chat_by_id(message.chat.id)
    if group:
        await bot.send_message(
            message.chat.id,
            f"Группа: {group.title}\nID группы: {group.chat_id}\n\nКоличество цитат:  {len(group.quotes)}\n"
            f"Последние добавленные: /get_quotes\n\nТекущие настройки:\n  Антиспам: {group.antispam}\n  "
            f"Ежедневные отчёты: {group.report}\n  Праздники: {group.reminder}")
    else:
        await bot.send_message(message.chat.id, "Группа не включена. Включить: /enable_stan")


@bot.message_handler(func=is_white_id, commands=["set_logging_level"], chat_types=["supergroup", "group"])
async def set_logging_level(message: types.Message):
    args = message.text.split()
    if args[-1] == '10':
        logger.setLevel(LOGGING_LEVEL_DEBUG)
        logging.info("[LEVEL] Установлен уровень DEBUG")
    else:
        logger.setLevel(LOGGING_LEVEL_INFO)
        logging.info("[LEVEL] Установлен уровень INFO")
