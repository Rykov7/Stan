from bs4 import BeautifulSoup
from urllib.request import urlopen

html = BeautifulSoup(urlopen('https://telegra.ph/pythonchatru-07-07'), 'lxml')


def get_rule(li):
    li = int(li)
    try:
        return html.find_all('li')[li - 1].text
    except IndexError:
        return 'Нет такого правила.'


if __name__ == '__main__':
    print(get_rule(1))
