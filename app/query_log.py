import csv
from os.path import exists
import datetime as dt


def logging(message):
    log_file_csv = f'logs/log_{dt.datetime.now().strftime("%Y-%m")}.csv'
    if not exists(log_file_csv):
        with open(log_file_csv, 'a') as f:
            logs = csv.writer(f)
            logs.writerow(['DATE AND TIME', 'ID', 'FIRST NAME', 'USERNAME',
                           'CHAT', 'LANG', 'PREMIUM', 'QUERY'])

    with open(log_file_csv, 'a') as f:
        logs = csv.writer(f)
        logs.writerow(
            [dt.datetime.now().strftime('%Y-%m-%d %H:%H'), message.from_user.id,
             message.from_user.first_name, message.from_user.username,
             message.chat.id, message.from_user.language_code, message.from_user.is_premium, message.text])
