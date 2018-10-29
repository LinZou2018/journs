import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, author, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.gscn.gansu",
        "newsType": "news",
        "title": title,
        "author": author,
        "release_time": timeout,
        "create_time": seconds(timeout, exist=True),
        "format_text": format_text,
        "source": "中国甘肃网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+)([\s\S]*?</div>)')
    timeout = re.findall(pattern, html)[0][0]
    pattern = re.compile('2018')
    exist = re.findall(pattern, timeout)
    if not exist:
        timeout = "20" + timeout
    pattern = re.compile('(<div class="a-footer">[\s\S]*?作者：)([\s\S]*?)(</span>)')
    author = re.findall(pattern, html)
    if author:
        author = author[0][1]
    else:
        author = ""
    pattern = re.compile('(<div class="a-container">)([\s\S]*?)(<div class="a-footer">)')
    format_text = re.findall(pattern, html)
    if format_text:
        format_text = format_text[0][1]
    else:
        pattern = re.compile('(<div id="content">)([\s\S]*?)(<!-- Baidu Button BEGIN -->)')
        format_text = re.findall(pattern, html)[0][1]
    format_text = re.sub("<div[\s\S]*?>", " ", format_text)
    format_text = re.sub("</div>", " ", format_text)
    storage(number, title, author, timeout, format_text)


def connect(url, number, title):
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return


def getURL(html):
    pattern = re.compile('<div id="content">[\s\S]*?</div>')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<li>[\s\S]*?</li>')
    msg = re.findall(pattern, data)
    for message in msg:
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.gscn.gansu"):
        #     return
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return


def starts():
    url = "http://gansu.gscn.com.cn/bwyc/index.html"
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        getURL(html)


if __name__ == '__main__':
    starts()