import shelve


def create_report_text():
    with shelve.open('chat_stats') as s:
        text = ''
        flooders = []
        for n in range(min(5, len(s['Messages']))):
            flooders.append(
                s['Messages'][sorted(s['Messages'], key=lambda a: s['Messages'][a]['Count'], reverse=True)[n]])

        for i, flooder in enumerate(flooders):
            username = flooder['Username']
            name = flooder['Name']
            count = flooder['Count']
            text += f'\n    {i + 1}. <a href="https://t.me/{username}">{name}</a> ({count})'
        report = f"""<code>Доброе утро, Мир!</code>
<b>За прошедшие сутки</b>

👮🏼 <b>Заблокировано</b>
    ├ <b>Пользователей: </b>{s['Banned']}
    └ <b>Сообщений: </b>{s['Deleted']}

🏆 <b>Почётные флудеры</b>{text}"""
    return report


def reset_report_stats():
    with shelve.open('chat_stats') as s:
        s['Messages'] = {}
        s['Banned'] = s['Deleted'] = 0
        return f"""
{s['Messages']=}
{s['Banned']=}
{s['Deleted']=}"""
