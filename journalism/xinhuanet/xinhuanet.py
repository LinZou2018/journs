import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.xinhuanet.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "新华网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number):
    pattern = re.compile('<div class="header">[\s\S]*?<div class="main">')
    head = re.findall(pattern, html)[0]
    pattern = re.compile('(<span>\s*?来源：)([\s\S]*?)(</span>)')
    source = re.findall(pattern, head)[0][1]
    pattern = re.compile('新华网')
    exist = re.findall(pattern, source)
    if not exist:
        return
    pattern = re.compile('(<div class="h-title">)([\s\S]*?)(</div>)')
    title = re.findall(pattern, head)[0][1]
    pattern = re.compile('\d+-\d+-\d+ \d+:\d+:\d+')
    timeout = re.findall(pattern, head)[0]
    pattern = re.compile('<div class="main">[\s\S]*?<div class="seo"')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<div id="p-detail">[\s\S]*?<div class="zan-wap">')
    text = re.findall(pattern, data)[0]
    pattern = re.compile('<p[\s\S]*?>[\s\S]*</p>')
    format_text = re.findall(pattern, text)[0]
    storage(number, title, timeout, format_text)


def createLinks(url, number):
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = reponse.text
        download(html, number)


def getURL(html):
    pattern = re.compile('<ul class="dataList">[\s\S]*?</ul>')
    data = re.findall(pattern, html)
    data = data[0]
    pattern = re.compile('<h3>[\s\S]*?</h3>')
    msg = re.findall(pattern, data)
    for message in msg:
        pattern = re.compile('(href=")([\s\S]*?)(")')
        url = re.findall(pattern, message)[0][1]
        pattern = re.compile("\d+")
        number = int(re.findall(pattern, url)[3])
        # if rechecking(number, source_url="com.xinhuanet.www"):
        #     return
        createLinks(url, number)


def starts():
    urls = ["http://www.news.cn/world/pl.htm", "http://www.news.cn/world/wmyl.htm",
            "http://www.news.cn/world/hqbl.htm", "http://www.news.cn/world/rw.htm",
            "http://www.xinhuanet.com/politics/rs.htm",
            "http://www.news.cn/politics/xhll.htm",
            "http://www.news.cn/info/index.htm", "http://www.news.cn/gangao/index.htm",
            "http://www.news.cn/food/index.htm"]
    for i in urls:
        url = i
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = reponse.text
            getURL(html)


if __name__ == '__main__':
    starts()