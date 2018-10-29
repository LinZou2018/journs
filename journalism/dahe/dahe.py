import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "cn.dahe.news",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "大河网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(id="pubtime_baidu">)(\d+年\d+月\d+日\d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    print(exist)
    if not exist:
        return
    pattern = re.compile('大河网')
    source = re.findall(pattern, exist[0][2])
    if not source:
        return
    timeout = exist[0][1]
    timestmap = time.strptime(timeout + ":00", "%Y年%m月%d日%H:%M:%S")
    timeout = time.strftime("%Y-%m-%d %H:%M:%S", timestmap)
    pattern = re.compile('(<div class="cl" id="mainCon">)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, timeout, format_text)


def connect(url, number, title):
    print(url)
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<ul class="newsleftul" id="content">[\s\S]*?</ul>')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<li>[\s\S]*?</li>')
    msg = re.findall(pattern, data)
    for message in msg:
        print(message)
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="cn.dahe.news"):
        #     return
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return


def starts():
    urls = ["https://news.dahe.cn/gn27/", "https://news.dahe.cn/gj27/", "https://news.dahe.cn/ty/",
            "https://news.dahe.cn/yl/", "https://news.dahe.cn/sh27/"]
    for i in urls:
        url = i
        response = requests.get(url, headers=headers.header())
        response.encoding = "utf-8"
        if response.status_code == 200:
            html = response.text
            getURL(html)


if __name__ == '__main__':
    starts()
