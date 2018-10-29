import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.workercn.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "中工网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+/\d+/\d+ \d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('界面')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    timestmap = time.strptime(timeout + ":00", "%Y/%m/%d %H:%M:%S")
    timeout = time.strftime("%Y-%m-%d %H:%M:%S", timestmap)
    pattern = re.compile('(<div class="article-content">)([\s\S]*>)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, timeout, format_text)


def connect(url, number, title):
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<div id="load-list"[\s\S]*?<div class="load-view">')
    data = re.findall(pattern, html)
    if not data:
        pattern = re.compile('<div id="load-qushi"[\s\S]*?<div class="load-view">')
        data = re.findall(pattern, html)
    pattern = re.compile('<h3>[\s\S]*?</h3>')
    msg = re.findall(pattern, data[0])
    for message in msg:
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.jiemian.www"):
        #     return
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return


def starts():
    urls = ["https://www.jiemian.com/lists/32.html", "https://www.jiemian.com/lists/71.html",
            "https://www.jiemian.com/lists/277.html", "https://www.jiemian.com/lists/174.html",
            "https://www.jiemian.com/lists/82.html", "https://www.jiemian.com/lists/31.html",
            "https://www.jiemian.com/lists/118.html", "https://www.jiemian.com/lists/65.html",]
    for i in urls:
        url = i
        response = requests.get(url, headers=headers.header())
        response.encoding = "utf-8"
        if response.status_code == 200:
            html = response.text
            getURL(html)


if __name__ == '__main__':
    starts()