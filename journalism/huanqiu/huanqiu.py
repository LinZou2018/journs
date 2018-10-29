import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds

def storage(number, title, author, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.xinhuanet.www",
        "newsType": "news",
        "title": title,
        "author": author,
        "release_time": timeout,
        "create_time": seconds(timeout, exist=True),
        "format_text": format_text,
        "source": "新华网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number):
    pattern = re.compile('<div class="con">[\s\S]*?<!-- 相关新闻 -->')
    data = re.findall(pattern, html)
    if data:
        data = data[0]
    else:
        return
    pattern = re.compile('<span class="la_t_b">[\s\S]*?</span>')
    source = re.findall(pattern, data)[0]
    pattern = re.compile('环球网')
    exist = re.findall(pattern, source)
    if not exist:
        return
    pattern = re.compile('(<h1 class="tle">)([\s\S]*?)(</h1>)')
    title = re.findall(pattern, data)[0][1]
    pattern = re.compile('(<span class="author">)([\s\S]*?)(</span>)')
    author = re.findall(pattern, data)
    if author:
        author = author[0][1]
    else:
        author = ""
    pattern = re.compile('(<span class="la_t_a">)([\s\S]*?)(</span>)')
    timeout = re.findall(pattern, data)[0][1]
    pattern = re.compile('(<div class="la_con">)([\s\S]*?)(<script type="text/javascript">)')
    format_text = re.findall(pattern, data)
    if format_text:
        format_text = format_text[0][1]
    else:
        pattern = re.compile('(<div class="la_con">)([\s\S]*?)(<div class="page")')
        format_text = re.findall(pattern, data)[0][1]
    storage(number, title, author, timeout, format_text)


def createLinks(url, number):
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = reponse.text
        download(html, number)


def getURL(html):
    pattern = re.compile('<ul class="listPicBox">[\s\S]*?</ul>')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<h3>[\s\S]*?</h3>')
    msg = re.findall(pattern, data)
    for message in msg:
        pattern = re.compile('(href=")([\s\S]*?)(")')
        url = re.findall(pattern, message)[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[2])
        # if rechecking(number, source_url="com.huanqiu.www"):
        #     return
        createLinks(url, number)


def starts():
    urls = ["http://world.huanqiu.com/article/", "http://mil.huanqiu.com/world/",
            "http://mil.huanqiu.com/strategysituation/", "http://china.huanqiu.com/article/",
            "http://taiwan.huanqiu.com/article/", "http://society.huanqiu.com/article/",
            "http://oversea.huanqiu.com/article/", "http://finance.huanqiu.com/jinr/",
            "http://finance.huanqiu.com/roll/", "http://finance.huanqiu.com/nengy/",
            "http://finance.huanqiu.com/zhengq/", "http://finance.huanqiu.com/gjcx/",
            "http://tech.huanqiu.com/internet/", "http://tech.huanqiu.com/comm/",
            "http://tech.huanqiu.com/science/","http://tech.huanqiu.com/fantasy/"]
    for i in urls:
        url = i
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = reponse.text
            getURL(html)


if __name__ == '__main__':
    starts()