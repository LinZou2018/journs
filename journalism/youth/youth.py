import re
import time
from lxml import etree

import requests
import headers
from mongodb_news import rechecking, storageDatabase


def storage(number, title, author, timeout, create_time, format_text, source):
    dicts = {
        "source_id": number,
        "source_url": "cn.youth.news",
        "newsType": "news",
        "title": title,
        "author": author,
        "release_time": timeout,
        "create_time": int(create_time) * 1000,
        "format_text": format_text,
        "source": source,
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number):
    pattern = re.compile('<div class="page_bt">[\s\S]*?</div>')
    data = re.findall(pattern, html)
    if not data:
        return
    msg = etree.HTML(data[0])
    text = etree.tostring(msg, method="text", encoding="utf8").decode("utf8").split()
    if "来源：" not in text:
        return
    num = text.index("来源：")
    source = text[num + 1]
    pattern = re.compile("中国青年网")
    exist = re.findall(pattern, source)
    if not exist:
        return
    pattern_time = re.compile("发稿时间：")
    pattern_author = re.compile("作者：")
    num_time = 0
    num_author = 0
    for i in text:
        exist = re.findall(pattern_time, i)
        if exist:
            num_time = text.index(i)
        exist = re.findall(pattern_author, i)
        if exist:
            num_author = text.index(i)
    title = ""
    for i in text[:num_time]:
        title += i + " "
    if num_time != 0:
        timeout = text[num_time] + " " + text[num_time + 1]
        pattern = re.compile("\d+-\d+-\d+ \d+:\d+:\d+")
        timeout = re.findall(pattern, timeout)[0]
        timeArray = time.strptime(timeout, "%Y-%m-%d %H:%M:%S")
        create_time = time.mktime(timeArray)
    else:
        timeout = ""
        create_time = ""
    if num_author != 0:
        pattern = re.compile("(作者：)([\s\S]*?)")
        author = re.findall(pattern, text[num_author])[0][1]
    else:
        author = ""
    pattern = re.compile("(<div class=TRS_Editor>)([\s\S]*?)(</div>)")
    format_text = re.findall(pattern, html)[0][1]
    pattern = re.compile('<iframe[\s\S]*</iframe>')
    format_text = re.sub(pattern, " ", format_text)
    storage(number, title, author, timeout, create_time, format_text, source)


def createLinks(incomplete_url, i, number):
    url = i + incomplete_url[2:]
    pattern = re.compile("http")
    exist = re.findall(pattern, incomplete_url)
    if exist:
        url = incomplete_url
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "gbk"
    if reponse.status_code == 200:
        html = reponse.text
        download(html, number)
    else:
        return True


def getURL(html, i):
    pattern = re.compile('<ul class="tj3_1">[\s\S]*?</ul>')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('(href=")([\s\S]*?)(")')
    urls = re.findall(pattern, data)
    for msg in urls:
        incomplete_url = msg[1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, incomplete_url)[2])
        # if rechecking(number, source_url="cn.youth.news"):
        #     return True
        data = createLinks(incomplete_url, i, number)
        if data:
            return True


def starts():
    urls = ["http://news.youth.cn/gn/", "http://news.youth.cn/sz/", "http://news.youth.cn/sh/",
            "http://news.youth.cn/gj/", "http://news.youth.cn/yl/", "http://news.youth.cn/bwyc/",
            "http://news.youth.cn/jsxw/"]
    for i in urls:
        n = 0
        while True:
            url = i
            if n > 0:
                url = url + "index_" + str(n) + ".htm"
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            if reponse.status_code == 200:
                html = reponse.text
                data = getURL(html, i)
                if data:
                    break
                n += 1


if __name__ == '__main__':
    starts()