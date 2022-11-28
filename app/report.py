import shelve


def create_report_text():
    top_users = ''
    flooders = []
    with shelve.open('chat_stats') as s:
        for n in range(min(3, len(s['Messages']))):
            top_user = s['Messages'][sorted(s['Messages'], key=lambda a: s['Messages'][a]['Count'], reverse=True)[n]]
            if top_user['Count'] >= 10:
                flooders.append(top_user)

        for i, flooder in enumerate(flooders):
            user = flooder["User"]
            name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
            top_users += f'\n  {i + 1}. <a href="tg://user?id={user.id}">{name}</a> ({flooder["Count"]})'
        report = f"""<code>Hello, World!</code> 🌍

<b>Заблокировано</b> ⛔
├ <b>Пользователей: </b>{s['Banned']}
└ <b>Сообщений: </b>{s['Deleted']}
"""
    if flooders:
        report += f"""
<b>Топ</b> 🏆{top_users}"""
    return report


def reset_report_stats():
    with shelve.open('chat_stats') as s:
        s['Messages'] = {}
        s['Banned'] = s['Deleted'] = 0
        return f"""
{s['Messages']=}
{s['Banned']=}
{s['Deleted']=}"""
