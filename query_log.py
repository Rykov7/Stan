import csv
import datetime as dt


def logging(message):
    date_and_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_file_csv = 'logs/logs.csv'
    with open(log_file_csv, 'a') as f:
        logs = csv.writer(f)
        logs.writerow(
            [date_and_time, message.from_user.id,
             message.from_user.first_name, message.from_user.username,
             message.chat.id, message.from_user.language_code, message.text])

