import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.yiren.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "文艺网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+年\d+月\d+日 \d+:\d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('艺人网')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    timestmap = time.strptime(timeout, "%Y年%m月%d日 %H:%M:%S")
    timeout = time.strftime("%Y-%m-%d %H:%M:%S", timestmap)
    pattern = re.compile('(<div class="article-content fontSizeBig yahei" >)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, timeout, format_text)


def connect(url, number, title):
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)


def getURL(html):
    pattern = re.compile('<div id="category"[\s\S]*?<!--@end文章内容-->')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<h1>[\s\S]*?</h1>')
    msg = re.findall(pattern, data)
    for message in msg:
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.yiren.www"):
        #     return True
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    urls = ["http://www.yiren.com.cn/star/list_1_%s.html", "http://www.yiren.com.cn/film/list_2_%s.html",
            "http://www.yiren.com.cn/tv/list_3_%s.html", "http://www.yiren.com.cn/music/list_4_%s.html",
            "http://www.yiren.com.cn/zongyi/list_5_%s.html", "http://www.yiren.com.cn/yule/list_6_%s.html",
            "http://www.yiren.com.cn/fashion/list_53_%s.html"]
    for i in urls:
        n = 1
        while True:
            url = i % n
            response = requests.get(url, headers=headers.header())
            response.encoding = "utf-8"
            if response.status_code == 200:
                html = response.text
                getURL(html)
                n += 1


if __name__ == '__main__':
    starts()