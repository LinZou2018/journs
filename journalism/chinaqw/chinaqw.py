import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.chinaqw.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "中国侨网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+年\d+月\d+日 \d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('中国侨网')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    timestmap = time.strptime(timeout + ":00", "%Y年%m月%d日 %H:%M:%S")
    timeout = time.strftime("%Y-%m-%d %H:%M:%S", timestmap)
    pattern = re.compile('(<div class="left_zw"[\s\S]*?<!--关键字-->)([\s\S]*?)(<div id="function_code_page">)')
    format_text = re.findall(pattern, html)
    if format_text:
        format_text = format_text[0][1]
    else:
        return
    storage(number, title, timeout, format_text)


def connect(url, number, title):
    pattern = re.compile('http')
    exist = re.findall(pattern, url)
    if exist:
        url = url
    else:
        url = "http://www.chinaqw.com" + url
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<ul >[\s\S]*?</ul')
    data = re.findall(pattern, html)
    for msg in data:
        pattern = re.compile('<li>[\s\S]*?</li>')
        dataOne = re.findall(pattern, msg)
        for message in dataOne:
            print(message)
            pattern = re.compile('(<a[\s\S]*?href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
            text = re.findall(pattern, message)
            if len(text) == 1:
                return True
            url = text[1][1]
            pattern = re.compile('\d+')
            number = int(re.findall(pattern, url)[-1])
            # if rechecking(number, source_url="com.chinaqw,www"):
            #     return True
            title = text[1][-2]
            mistake = connect(url, number, title)
            if mistake:
                return True


def starts():
    urls = "http://www.chinaqw.com/scroll-news/news%s.shtml"
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
