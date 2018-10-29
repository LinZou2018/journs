import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.eastyule.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "东方娱乐网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    print(exist)
    if not exist:
        return
    pattern = re.compile('东方')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    pattern = re.compile('(<div id="endText">)([\s\S]*?)(<script)')
    format_text = re.findall(pattern, html)[0][1]
    format_text = re.sub("<div[\s\S]*?>", "<p>", format_text)
    format_text = re.sub("</div>", "</p>", format_text)
    storage(number, title, timeout, format_text)


def connect(url, number, title):
    response = requests.get(url, headers=headers.header())
    response.encoding = "gbk"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<ul class="c_list">[\s\S]*?</ul>')
    data = re.findall(pattern, html)
    pattern = re.compile('<li>[\s\S]*?</li>')
    msg = re.findall(pattern, data[0])
    for message in msg:
        print(message)
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.eastyule.www"):
        #     return
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    urls = ["http://www.eastyule.com/news/star/index.html", "http://www.eastyule.com/news/movie/index.html",
            "http://www.eastyule.com/news/music/index.html", "http://www.eastyule.com/news/zongyi/index.html"]
    for i in urls:
        n = 1
        while True:
            if n == 1:
                url = i
            else:
                url = re.sub("index", str(n), i)
            response = requests.get(url, headers=headers.header())
            response.encoding = "gbk"
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