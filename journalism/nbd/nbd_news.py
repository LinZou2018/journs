import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, author, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.nbd.www",
        "newsType": "news",
        "title": title,
        "author": author,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "每经网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(<p class="u-time">[\s\S]*?)(\d+-\d+-\d+ \d+:\d+:\d+)')
    exist = re.findall(pattern, html)
    print(exist)
    if not exist:
        return
    pattern = re.compile('每日经济新闻')
    source = re.findall(pattern, exist[0][0])
    if not source:
        return
    print("5555")
    timeout = exist[0][1]
    pattern = re.compile('(<div class="g-articl-text">)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
    pattern = re.compile('(<div class="u-editor">[\s\S]*?<span>)([\s\S]*?)(</span>[\s\S]*?</div>)')
    author = re.findall(pattern, html)
    if author:
        author = author[0][1]
    else:
        author = ""
    storage(number, title, author, timeout, format_text)


def connect(url, number, title):
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        print("4444")
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<div class="m-list">[\s\S]*?</ul>')
    data = re.findall(pattern, html)
    for msg in data:
        pattern = re.compile('<li[\s\S]*?>[\s\S]*?</li>')
        concentrate = re.findall(pattern, msg)
        print("2222")
        for message in concentrate:
            pattern = re.compile('(href=")([\s\S]*?)(")')
            url = re.findall(pattern, message)[0][1]
            pattern = re.compile('\d+')
            number = int(re.findall(pattern, url)[-1])
            # if rechecking(number, source_url="com.nbd.www"):
            #     return True
            pattern = re.compile('(<a[\s\S]*?>)([\s\S]*?)(</a>)')
            title = re.findall(pattern, message)[0][1]
            print("3333")
            mistake = connect(url, number, title)
            if mistake:
                return True


def starts():
    urls = ["http://www.nbd.com.cn/columns/3/page/%s", "http://www.nbd.com.cn/columns/697/page/%s"]
    for i in urls:
        n = 1
        while True:
            url = i % n
            response = requests.get(url, headers=headers.header())
            response.encoding = "utf-8"
            if response.status_code == 200:
                print("1111")
                html = response.text
                mistake = getURL(html)
                if mistake:
                    break
                n += 1
            else:
                break


if __name__ == '__main__':
    starts()