import html
import logging
import os
import random
import shelve
from pathlib import Path

from .config import ROLLBACK
from .constants import DATA, types


def increment(chat_id: int, banned: bool = True):
    """
    Увеличивает счетчик банов или удаленных
    """
    category = "Banned" if banned else "Deleted"
    with shelve.open(f"{DATA}{chat_id}", writeback=True) as shelve_db:
        shelve_db[category] += 1


def create_report_text(chat_id):
    report = ""
    top_users = ""
    flooders = []
    spammer_icons = ('🐷', '🐒', '🐔')
    current_spammer_face = random.choice(spammer_icons)
    if os.path.exists(f"{DATA}{chat_id}.db"):
        with shelve.open(f"{DATA}{chat_id}", writeback=True) as s:
            for user_id in ROLLBACK:
                if user_id in s["Messages"] and s["Messages"][user_id]["Count"] > 10:
                    s["Messages"][user_id]["Count"] //= 3

            for n in range(min(3, len(s["Messages"]))):
                top_user = s["Messages"][
                    sorted(
                        s["Messages"],
                        key=lambda a: s["Messages"][a]["Count"],
                        reverse=True,
                    )[n]
                ]
                if top_user["Count"] >= 5:
                    flooders.append(top_user)

            for i, flooder in enumerate(flooders):
                user = flooder["User"]
                name = (
                    f"{user.first_name} {user.last_name}"
                    if user.last_name
                    else user.first_name
                )
                top_users += f'\n{i + 1}. {html.escape(name)} [{flooder["Count"]}]'

            if len(flooders) >= 3 or s["Banned"] or s["Deleted"]:
                report = f"<b>H</b>ello, <b>W</b>orld!\n"
            if len(flooders) >= 3:
                report += f"{top_users}\n"
            if s["Banned"]:
                report += f"""
<b> Криптоидов поймано:</b> {s['Banned']}
  └ [ {s['Banned'] * current_spammer_face} ] 
"""
        return report
    else:
        return f"Невозможно получить статистику.\n{DATA}{chat_id}.db не существует, возможно запрос в приватном чате. "


def reset_report_stats(chat_id):
    with shelve.open(f"{DATA}{chat_id}") as shelve_db:
        shelve_db["Messages"] = {}
        shelve_db["Banned"] = 0
        shelve_db["Deleted"] = 0
        return f"""Chat ID: {chat_id}

{shelve_db['Messages']=}
{shelve_db['Banned']=}
{shelve_db['Deleted']=}"""


def update_stats(message: types.Message):
    if not Path(f"{DATA}{message.chat.id}").exists():
        reset_report_stats(message.chat.id)
    with shelve.open(f"{DATA}{message.chat.id}", writeback=True) as shelve_db:
        if "Messages" not in shelve_db:
            reset_report_stats(message.chat.id)
        if message.from_user.id not in shelve_db["Messages"]:
            shelve_db["Messages"][message.from_user.id] = {"User": message.from_user, "Count": 1}
            logging.info(f"[{message.chat.title[:10]}] [{message.from_user.id}] {message.from_user.first_name}")
        else:
            shelve_db["Messages"][message.from_user.id]["Count"] += 1
