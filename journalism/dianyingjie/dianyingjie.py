import re
import json
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(message, timeout, format_text):
    dicts = {
        "source_id": int(message["contentid"]),
        "source_url": "com.dianyingjie.www",
        "newsType": "news",
        "title": message["title"],
        "release_time": timeout,
        "create_time": seconds(timeout, exist=True),
        "format_text": format_text,
        "source": "电影网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, message):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('电影界')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    pattern = re.compile('(<div class="article-content fontSizeSmall BSHARE_POP">)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)
    storage(message, timeout, format_text)


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
    pattern = re.compile('{[\s\S]*}')
    data = re.findall(pattern, html)[0]
    data = json.loads(data)
    msg = data["data"]
    for message in msg:
        number = int(message["contentid"])
        # if rechecking(number, source_url="com.dianyingjie.www"):
        #     return True
        mistake = connect(message)
        if mistake:
            return True


def starts():
    n = 1
    while True:
        url = "http://app.dianyingjie.com/roll.php?do=query&size=20&page=" + str(n)
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