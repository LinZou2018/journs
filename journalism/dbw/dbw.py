import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, author, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.dbw.heilongjiang",
        "newsType": "news",
        "title": title,
        "author": author,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "东北网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile("东北网")
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    pattern = re.compile('(作者：)([\s\S]*?)(</div>)')
    author = re.findall(pattern, exist[0][1])
    pattern = re.compile('<div id="p-detail">[\s\S]*?<div id="gjc">')
    format_text = re.findall(pattern, html)[0]
    format_text = re.sub('<div[\s\S]*?>', " ", format_text)
    format_text = re.sub('<script[\s\S]*?>[\s\S]*?</script>', " ", format_text)
    storage(number, title, author, timeout, format_text)


def connect(url, number, title):
    response = requests.get(url, headers=headers.header())
    response.encoding = "gbk"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<ul class="list-title">[\s\S]*?</ul>')
    text = re.findall(pattern, html)[0]
    pattern = re.compile('<li>[\s\S]*?</li>')
    data = re.findall(pattern, text)
    for message in data:
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        msg = re.findall(pattern, message)
        url = "http:" + msg[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="cn.dbw.heilongjiang"):
        #     return "end"
        title = msg[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return "end"


def starts():
    url = "https://heilongjiang.dbw.cn/system/count/0015037/000000000000/count_page_list_0015037000000000000.js"
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        pattern = re.compile('(maxpage = )(\d+)(;)')
        num = int(re.findall(pattern, html)[0][1])
    else:
        return
    n = 0
    while True:
        if n == 0:
            url = "https://heilongjiang.dbw.cn/rc/index.shtml"
        else:
            page = num - n
            url = "https://heilongjiang.dbw.cn/system/count//0015037/000000000000/000/000/c0015037000000000000_000000%s.shtml" % page
        response = requests.get(url, headers=headers.header())
        response.encoding = "gbk"
        if response.status_code == 200:
            html = response.text
            mistake = getURL(html)
            if mistake == "end":
                break
            n += 1
        else:
            break


if __name__ == '__main__':
    starts()