import re
import time
import json
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, data, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.qq.news",
        "newsType": "news",
        "title": data["title"],
        "release_time": data["pubtime"],
        "create_time": seconds(data["pubtime"]),
        "format_text": format_text,
        "source": "腾讯",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html):
    pattern = re.compile('(window.DATA = )({[\s\S]*?})')
    exist = re.findall(pattern, html)
    if not exist:
        return
    data = json.loads(exist[0][1])
    pattern = re.compile('腾讯')
    source = re.findall(pattern, data["media"])
    if not source:
        return
    number = data["article_id"]
    # if rechecking(number, source_url="com.qq.news"):
    #     return True
    pattern = re.compile('(<div class="content-article">)([\s\S]*?)(<div)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, data, format_text)


def connect(url):
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html)


def getURL(html):
    pattern = re.compile('<div id="List">[\s\S]*?<div id="Right">')
    data = re.findall(pattern, html)[0]
    print(data)
    pattern = re.compile('<li[\s\S]*?>[\s\S]*?</li>')
    msg = re.findall(pattern, data)
    print(msg)
    for message in msg:
        pattern = re.compile('(href=")([\s\S]*?)(")')
        url = re.findall(pattern, message)[0][1]
        connect(url)


def starts():
    urls = ["https://new.qq.com/ch/world/", "https://new.qq.com/ch/ent/", "https://new.qq.com/ch/sports/",
            "https://new.qq.com/ch/milite/", "https://new.qq.com/ch/sports_nba/", "https://new.qq.com/ch/tech/",
            "https://new.qq.com/ch/finance/", "https://new.qq.com/ch/fashion/", "https://new.qq.com/ch/games/",
            "https://new.qq.com/ch/comic/"]
    for i in urls:
        url = i
        response = requests.get(url, headers=headers.header())
        response.encoding = "utf-8"
        if response.status_code == 200:
            html = response.text
            getURL(html)


if __name__ == '__main__':
    starts()