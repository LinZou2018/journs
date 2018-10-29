import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, author, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "cn.cri.news",
        "newsType": "news",
        "title": title,
        "author": author,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "国内在线",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title, timeout):
    pattern = re.compile('(<span id="aeditor"[\s\S]*?>编辑：)([\s\S]*?)(</span>)')
    author = re.findall(pattern, html)
    if author:
        author = author[0][1]
    else:
        author = ""
    pattern = re.compile('(<div id="abody"[\s\S]*?>)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, author, timeout, format_text)


def connect(url, number, title, timeout):
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = reponse.text
        download(html, number, title, timeout)
    else:
        return True


def getURL(html):
    pattern = re.compile('<div class="text">[\s\S]*?</div>')
    data = re.findall(pattern, html)
    for message in data:
        pattern = re.compile('(href=")([\s\S]*?)(")')
        portion = re.findall(pattern, message)[0][1]
        pattern = re.compile('(/)([\s\S]*?)(.html)')
        number = re.findall(pattern, portion)[0][1]
        # if rechecking(number, source_url="cn.cri.news"):
        #     return True
        url = "http://news.cri.cn" + portion
        pattern = re.compile('(<a[\s\S]*?>)([\s\S]*?)(</a>)')
        title = re.findall(pattern, message)[0][1]
        pattern = re.compile('(<i>)([\s\S]*?)(</i>)')
        timeout = re.findall(pattern, message)[0][1]
        msg = connect(url, number, title, timeout)
        if msg:
            return True


def starts():
    n = 1
    while True:
        if n == 1:
            url = "http://news.cri.cn/exclusive"
        else:
            url = "http://news.cri.cn/exclusive-%s" % n
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = reponse.text
            data = getURL(html)
            if data:
                break
            n += 1
        else:
            break


if __name__ == '__main__':
    starts()