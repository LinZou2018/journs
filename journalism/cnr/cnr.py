import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, author, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.cmr.news",
        "newsType": "news",
        "title": title,
        "author": author,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "央广网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('央广网')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    pattern = re.compile('(<div class="Custom_UnionStyle">)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)
    if format_text:
        format_text = format_text[0][1]
    else:
        return
    pattern = re.compile('(<div class="editor">编辑：\s+)([\s\S]*?)(\s+</div>)')
    author = re.findall(pattern, html)[0][1]
    storage(number, title, author, timeout, format_text)


def connect(url, number, title):
    response = requests.get(url, headers=headers.header())
    response.encoding = "gb2312"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<TRS_Documents[\s\S]*?</ul>')
    data = re.findall(pattern, html)
    pattern = re.compile('<a[\s\S]*?</a>')
    msg = re.findall(pattern, data[0])
    for message in msg:
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.cnr.news"):
        #     return True
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    urls = "http://kuaixun.cnr.cn/index_1.html?day="
    timeout = time.localtime()
    page = timeout.tm_mday
    while True:
        url = urls + str(timeout.tm_year) + "," + str(timeout.tm_mon) + "," + str(page)
        response = requests.get(url, headers=headers.header())
        response.encoding = "utf-8"
        if response.status_code == 200:
            html = response.text
            mistake = getURL(html)
            if mistake:
                break
            if page == 1:
                timeout.tm_mon -= 1
            else:
                page -= 1
        else:
            break


if __name__ == '__main__':
    starts()