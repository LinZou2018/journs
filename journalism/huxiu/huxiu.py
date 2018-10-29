import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


header = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "80",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "www.huxiu.com",
    "Origin": "https://www.huxiu.com",
    "Referer": "https://www.huxiu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


def storage(number, title, author, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.huxiu.www",
        "newsType": "news",
        "title": title,
        "author": author,
        "release_time": timeout,
        "create_time": seconds(timeout, exist=True),
        "format_text": format_text,
        "source": "虎嗅",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(<div[\s\S]*?)(\d+-\d+-\d+ \d+:\d+)')
    exist = re.findall(pattern, html)[0]
    timeout = exist[1]
    pattern = re.compile('(<span class="author-name">[\s\S]*?>)([\s\S]*?)(</a>)')
    author = re.findall(pattern, html)
    if author:
        author = author[0][1]
    else:
        author = ""
    pattern = re.compile('(<div id="article_content[\s\S]*?>)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, author, timeout, format_text)


def connect(url, number, title):
    url = "https://www.huxiu.com" + url
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return "end"



def getURL(html, n):
    last_dateline = ""
    if n == 1:
        pattern = re.compile('<div class="mod-info-flow">[\s\S]*?点击加载更多')
        msg = re.findall(pattern, html)[0]
    else:
        pattern = re.compile('data[\s\S]*?last_dateline')
        msg = re.findall(pattern, html)[0]
        pattern = re.compile('(last_dateline\S)("[\s\S]*?")')
        last_dateline = re.findall(pattern, html)[0][1]
    pattern = re.compile('<h2>[\s\S]*?</h2>')
    text_list = re.findall(pattern, msg)
    url = ""
    for message in text_list:
        pattern = re.compile('(href=")([\s\S]*?)(")')
        url = re.findall(pattern, message)[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[0])
        # if rechecking(number, source_url="com.huxiu.www"):
        #     return "end"
        pattern = re.compile('(<a[\s\S]*?>)([\s\S]*?)(</a>)')
        title = re.findall(pattern, message)[0][1]
        mistake = connect(url, number, title)
        if mistake:
            return "end"
    if n == 1:
        url = "https://www.huxiu.com" + url
        response = requests.get(url, headers=headers.header())
        response.encoding = "utf-8"
        html = response.text
        pattern = re.compile('(<div[\s\S]*?)(\d+-\d+-\d+ \d+:\d+)')
        exist = re.findall(pattern, html)[0]
        timeout = exist[1] + ":00"
        timeArray = time.strptime(timeout, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        last_dateline = int(timestamp)
    return last_dateline


def starts():
    url = "https://www.huxiu.com/v2_action/article_list"
    n = 1
    last_dateline = ""
    while True:
        data = {
            "huxiu_hash_code": "9501c2ced764ebbe029807a9f17790fa",
            "page": str(n),
            "last_dateline": str(last_dateline)
        }
        if n == 1:
            url = "https://www.huxiu.com"
            response = requests.get(url, headers=headers.header())
        else:
            response = requests.get(url, data=data, headers=header)
        response.encoding = "utf-8"
        if response.status_code == 200:
            html = response.text
            mistake = getURL(html, n)
            if mistake == "end":
                break
            last_dateline = mistake
            n += 1
        else:
            break


if __name__ == '__main__':
    starts()