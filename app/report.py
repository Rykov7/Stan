import shelve


def create_report_text():
    with shelve.open('chat_stats') as s:
        text = ''
        flooders = []
        for n in range(min(3, len(s['Messages']))):
            flooders.append(
                s['Messages'][sorted(s['Messages'], key=lambda a: s['Messages'][a]['Count'], reverse=True)[n]])

        for i, flooder in enumerate(flooders):
            user = flooder["User"]
            name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
            text += f'\n  {i + 1}. <a href="tg://user?id={user.id}">{name}</a> ({flooder["Count"]})'
        report = f"""<code>Доброе утро, Мир!</code>
<b>За прошлые сутки</b>

<b>Заблокировано</b>
├ <b>Пользователей: </b>{s['Banned']}
└ <b>Сообщений: </b>{s['Deleted']}

<b>Главные флудеры</b> 🏆{text}"""
    return report


def reset_report_stats():
    with shelve.open('chat_stats') as s:
        s['Messages'] = {}
        s['Banned'] = s['Deleted'] = 0
        return f"""
{s['Messages']=}
{s['Banned']=}
{s['Deleted']=}"""
