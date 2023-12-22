from urllib.request import urlopen

from bs4 import BeautifulSoup

from .config import RULES_URL

html = BeautifulSoup(urlopen(RULES_URL), "lxml")


def fetch_rule(li):
    li = int(li)
    lis = html.find_all("li")
    if li <= len(lis):
        return lis[li - 1].text
    else:
        return f"Пока не придумали."
