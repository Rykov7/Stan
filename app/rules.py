from bs4 import BeautifulSoup
from urllib.request import urlopen

html = BeautifulSoup(urlopen("https://telegra.ph/pythonchatru-07-07"), "lxml")


def fetch_rule(li):
    li = int(li)
    lis = html.find_all("li")
    if li <= len(lis):
        return lis[li - 1].text
    else:
        return f"Пока не придумали."
