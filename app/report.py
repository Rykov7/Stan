import html
import shelve
import os
from .config import DATA, ROLLBACK


def create_report_text(chat_id):
    report = ""
    top_users = ""
    flooders = []
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
                report = f"Hello, World!\n"
            if len(flooders) >= 3:
                report += f"{top_users}\n"
            if s["Banned"]:
                report += f"""
<b> Спамеров в топке:</b> {s['Banned']}
  └ [ {s['Banned']*'🐒'} ] 
"""
        return report
    else:
        return f"Невозможно получить статистику.\n{DATA}{chat_id}.db не существует, возможно запрос в приватном чате. "


def reset_report_stats(chat_id):
    with shelve.open(f"{DATA}{chat_id}") as s:
        s["Messages"] = {}
        s["Banned"] = 0
        s["Deleted"] = 0
        return f"""Chat ID: {chat_id}

{s['Messages']=}
{s['Banned']=}
{s['Deleted']=}"""
