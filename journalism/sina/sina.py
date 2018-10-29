import re
import json
import requests
import headers
from mongodb_news import rechecking, storageDatabase
import time


def storage(message, format_text):
    dicts = {
        "source_id": int(message["oid"]),
        "source_url": "com.sina.news",
        "newsType": "news",
        "title": message["title"],
        "release_time": time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(message["intime"]))),
        "create_time": int(message["intime"]) * 1000,
        "format_text": format_text,
        "source": "新浪",
    }
    print(dicts)
    # storageDatabase(dicts)



def download(html, message):
    pattern = re.compile('(<div class="article" id="article">)([\s\S]*?<p class="show_author">[\s\S]*?</p>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    format_text = exist[0][1]
    format_text = re.sub('<div[\s\S]*?>', '<p>', format_text)
    format_text = re.sub('</div>', '</p>', format_text)
    storage(message, format_text)


def connect(message):
    url = message["url"]
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, message)
    else:
        return True


def getURL(html):
    data = json.loads(html)
    print(data)
    msg = data["result"]
    data = msg["data"]
    for message in data:
        number = int(message["oid"])
        # if rechecking(number, source_url="com.sina.news"):
        #     return True
        media_name = message["media_name"]
        pattern = re.compile("新浪")
        source = re.findall(pattern, media_name)
        if not source:
            continue
        mistake = connect(message)
        if mistake:
            return True


def starts():
    urls = "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page=%s"
    n = 1
    while True:
        url = urls % n
        response = requests.get(url, headers=headers.header())
        response.encoding = "utf-8"
        if response.status_code == 200:
            html = response.text
            mistake = getURL(html)
            if mistake:
                break
            n += 1
        else:
            break


if __name__ == '__main__':
    starts()