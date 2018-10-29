import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.ittime.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "IT时代网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+年\d+月\d+日 \d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('cnBeta')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    timeArray = time.strptime(timeout + ":00", "%Y年%m月%d日 %H:%M:%S")
    timeout = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    pattern = re.compile('(<div class="article-summary">[\s\S]*?)(<div class="tac">)')
    format_text = re.findall(pattern, html)[0][0]
    format_text = re.sub('<div[\s\S]*?>', '<p>', format_text)
    format_text = re.sub('</div>', '</p>', format_text)
    storage(number, title, timeout, format_text)


def connect(url, number, title):
    url = "http:" + url
    print(url)
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<dl>[\s\S]*?</dl>')
    data = re.findall(pattern, html)
    for message in data:
        pattern = re.compile('(<dt><a href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a></dt>)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('http')
        exist = re.findall(pattern, url)
        if exist:
            continue
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.cnbeta.www"):
        #     return True
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return


def starts():
    urls = ["https://www.cnbeta.com/category/movie.htm", "https://www.cnbeta.com/category/music.htm",
            "https://www.cnbeta.com/category/game.htm", "https://www.cnbeta.com/category/comic.htm",
            "https://www.cnbeta.com/category/funny.htm"]
    for i in urls:
        url = i
        response = requests.get(url, headers=headers.header())
        response.encoding = "utf-8"
        if response.status_code == 200:
            html = response.text
            getURL(html)


if __name__ == '__main__':
    starts()