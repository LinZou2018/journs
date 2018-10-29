import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, author, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.shobserver.www",
        "newsType": "news",
        "title": title,
        "author": author,
        "release_time": timeout,
        "create_time": seconds(timeout, exist=True),
        "format_text": format_text,
        "source": "上观",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number):
    pattern = re.compile('(<div[\s\S]*?)(\d+-\d+-\d+ \d+:\d+)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile("上观")
    source = re.findall(pattern, exist[0][0])
    if not source:
        return
    timeout = exist[0][1]
    pattern = re.compile('(作者：[\s\S]*?>)([\s\S]*?)(</span>)')
    author = re.findall(pattern, exist[0][0])[0][1]
    pattern = re.compile('(<div class="wz_contents">)([\s\S]*?)(</div>)')
    title = re.findall(pattern, html)[0][1]
    pattern = re.compile('(<div id="newscontents"[\s\S]*?>)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, author, timeout, format_text)


def connect(url, number):
    url = "https://www.shobserver.com" + url
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number)


def getURL(html):
    pattern = re.compile('<div class="center">[\s\S]*?上一页')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<div class="chengshi_img">[\s\S]*?</div>')
    text_list = re.findall(pattern, data)
    for message in text_list:
        pattern = re.compile('(href=")([\s\S]*?)(")')
        url = re.findall(pattern, message)[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[0])
        # if rechecking(number, source_url="com.shobserver.www"):
        #     return True
        connect(url, number)


def starts():
    urls = ["https://www.shobserver.com/news/list?section=1&page=%s", "https://www.shobserver.com/news/list?section=2&page=%s",
            "https://www.shobserver.com/news/list?section=35&page=%s", "https://www.shobserver.com/news/list?section=22&page=%s",
            "https://www.shobserver.com/news/list?section=4&page=%s", "https://www.shobserver.com/news/list?section=21&page=%s",
            "https://www.shobserver.com/news/list?section=40&page=%s", "https://www.shobserver.com/news/list?section=41&page=%s"]
    for i in urls:
        n = 1
        while True:
            url = i % n
            response = requests.get(url, headers=headers.header())
            response.encoding = "utf-8"
            if response.status_code == 200:
                html = response.text
                getURL(html)


if __name__ == '__main__':
    starts()