import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.artsbj.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "北京文艺网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+/\d+/\d+ \d+:\d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('文艺网')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    timestmap = time.strptime(timeout, "%Y/%m/%d %H:%M:%S")
    timeout = time.strftime("%Y-%m-%d %H:%M:%S", timestmap)
    pattern = re.compile('(<div id="MyContent">)([\s\S]*?)(<div)')
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
    pattern = re.compile('<ul class="dotUl">[\s\S]*?</ul>')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<li>[\s\S]*?</li>')
    msg = re.findall(pattern, data)
    for message in msg:
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern , message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[1])
        # if rechecking(number, source_url="com.artsbj.www"):
        #     return True
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    urls = ["http://www.artsbj.com/list-17-%s.html", "http://www.artsbj.com/list-18-%s.html",
            "http://www.artsbj.com/list-19-%s.html", "http://www.artsbj.com/list-20-%s.html",
            "http://www.artsbj.com/list-21-%s.html", "http://www.artsbj.com/list-22-%s.html",
            "http://www.artsbj.com/list-23-%s.html", "http://www.artsbj.com/list-24-%s.html"]
    for i in urls:
        n = 1
        while True:
            url = i % n
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