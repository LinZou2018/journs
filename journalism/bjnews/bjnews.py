import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, author, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.bjnews.www",
        "newsType": "news",
        "title": title,
        "author":author,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "新京报网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('新京报')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    pattern = re.compile('(作者：)([\s\S]*?)(</span>)')
    author = re.findall(pattern, exist[0][1])[0][1]
    pattern = re.compile('(<div class="content">)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, author, timeout, format_text)


def connect(url, number, title):
    url = "http://www.bjnews.com.cn" + url
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<ul id="news_ul">[\s\S]*?</ul>')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<li>[\s\S]*?</li>')
    msg = re.findall(pattern, data)
    for message in msg:
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.bjnews.www"):
        #     return True
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    n = 1
    while True:
        url = "http://www.bjnews.com.cn/roll?page=" + str(n)
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