import shelve
import os
from .config import DATA


def create_report_text(chat_id):
    report = ''
    top_users = ''
    flooders = []
    if os.path.exists(f'{DATA}{chat_id}.db'):
        with shelve.open(f'{DATA}{chat_id}') as s:
            for n in range(min(3, len(s['Messages']))):
                top_user = s['Messages'][sorted(s['Messages'], key=lambda a: s['Messages'][a]['Count'], reverse=True)[n]]
                if top_user['Count'] >= 10:
                    flooders.append(top_user)

            for i, flooder in enumerate(flooders):
                user = flooder["User"]
                name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
                top_users += f'\n  {i + 1}. <a href="tg://user?id={user.id}">{name}</a> ({flooder["Count"]})'

            if len(flooders) >= 3:
                report += f"<code>Hello, World!</code> 🌍"
                report += f"\n<b>Топ</b> 🗣{top_users}"

            if s['Banned'] or s['Deleted']:
                report += f"""
<b>Заблокировано</b> ⛔
├ <b>Пользователей: </b>{s['Banned']}
└ <b>Сообщений: </b>{s['Deleted']}
"""
        return report
    else:
        return f'Невозможно получить статистику.\n{DATA}{chat_id}.db не существует, возможно запрос в приватном чате. '


def reset_report_stats(chat_id):
    with shelve.open(f'{DATA}{chat_id}') as s:
        s['Messages'] = {}
        s['Banned'] = 0
        s['Deleted'] = 0
        return f"""Chat ID: {chat_id}

{s['Messages']=}
{s['Banned']=}
{s['Deleted']=}"""
