import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.asiacool.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "Asiacool",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('亚洲')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    pattern = re.compile('(<div id="content">)([\s\S]*?)(<div id="pages)"')
    format_text = re.findall(pattern, html)[0][1]
    format_text = re.sub("div", "p", format_text)
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
    pattern = re.compile('<div id="LBMBL" class="MBL">[\s\S]*?</ul>')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<li >[\s\S]*?</li>')
    msg = re.findall(pattern, data)
    for message in msg:
        pattern = re.compile('<div class="title">[\s\S]*?</div>')
        title_text = re.findall(pattern, message)[0]
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, title_text)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.asiacool.www"):
        #     return
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    urls = ["http://www.asiacool.com/news/list_9.html", "http://www.asiacool.com/news/list_10.html",
            "http://www.asiacool.com/news/list_11.html", "http://www.asiacool.com/news/list_12.html",
            "http://www.asiacool.com/news/list_13.html", "http://www.asiacool.com/news/list_14.html"]
    for i in urls:
        n = 1
        while True:
            if n == 1:
                url = i
            else:
                page = "_" + str(n) + ".html"
                url = re.sub(".html", page, i)
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