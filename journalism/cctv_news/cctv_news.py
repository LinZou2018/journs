import re
import json
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(message, format_text):
    dicts = {
        "source_id": message["id"],
        "source_url": "com.cctv.news",
        "newsType": "news",
        "title": message["title"],
        "release_time": message["dateTime"],
        "create_time": seconds(message["dateTime"], exist=True),
        "format_text": format_text,
        "source": "央视网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, message):
    pattern = re.compile('<i>来源：[\s\S]*?</i>')
    source = re.findall(pattern, html)
    if source:
        source = source[0]
    else:
        return
    pattern = re.compile('央视网')
    exist = re.findall(pattern, source)
    if not exist:
        return
    pattern = re.compile('(<!--repaste.body.begin-->)([\s\S]*?)(<!--repaste.body.end-->)')
    format_text = re.findall(pattern, html)
    storage(message, format_text)



def connect(message):
    url = message["url"]
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    print(url)
    if reponse.status_code == 200:
        html = reponse.text
        download(html, message)


def getURL(html):
    data = json.loads(html)
    roll = data["rollData"]
    for message in roll:
        number = message["id"]
        # if rechecking(number, source_url="com.cctv.news"):
        #     return True
        connect(message)


def starts():
    urls = ["http://news.cctv.com/china/data/index.json", "http://news.cctv.com/world/data/index.json",
            "http://military.cctv.com/data/index.json", "http://news.cctv.com/tech/data/index.json",
            "http://news.cctv.com/society/data/index.json", "http://news.cctv.com/law/data/index.json",
            "http://news.cctv.com/ent/data/index.json"]
    for i in urls:
        url = i
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = reponse.text
            getURL(html)


if __name__ == '__main__':
    starts()