import re
import json
import requests
import headers
from mongodb_news import rechecking, storageDatabase


def storage(message, timeout, format_text):
    dicts = {
        "source_id": int(message["contentid"]),
        "source_url": "com.taihainet.www",
        "newsType": "news",
        "title": message["title"],
        "release_time": timeout,
        "create_time": int(message["published"]) * 1000,
        "format_text": format_text,
        "source": "华夏经纬网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, message):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('台海网')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    pattern = re.compile('(<div class="article-content">)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
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
    pattern = re.compile('\{[\s\S]*\}')
    data = re.findall(pattern, html)[0]
    data = json.loads(data)
    text = data["data"]
    for message in text:
        number = int(message["contentid"])
        # if rechecking(number, source_url="com.taihainet.www"):
        #     return True
        mistake = connect(message)
        if mistake:
            return True


def starts():
    urls = "http://app.taihainet.com/roll.php?do=query&callback=jsonp1539828763543&_=1539830476615&channel=0&date=2018-10-18&size=50&page="
    n = 1
    while True:
        url = urls + str(n)
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