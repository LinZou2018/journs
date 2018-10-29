import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.kankanews.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "看看新闻",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(<div class="infor">[\s\S]*?)(\d+-\d+-\d+ \d+:\d+:\d+)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('看看')
    source = re.findall(pattern, exist[0][0])
    if not source:
        return
    timeout = exist[0][1]
    pattern = re.compile('(<div class="textBody">)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, timeout, format_text)


def connect(url, number, title):
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<div class="right infor">[\s\S]*?</div>')
    data = re.findall(pattern, html)
    pattern = re.compile('<ul class="clearfix conlist">[\s\S]*?</ul>')
    msg = re.findall(pattern, html)[0]
    pattern = re.compile('<h1>[\s\S]*?</li>')
    msgli = re.findall(pattern, msg)
    data = data + msgli
    for message in data:
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.kankanews.www"):
        #     return True
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    urls = ["http://www.kankanews.com/list/xinwen/498", "http://www.kankanews.com/list/xinwen/508",
            "http://www.kankanews.com/list/xinwen/511", "http://www.kankanews.com/list/xinwen/517",
            "http://www.kankanews.com/list/xinwen/519", "http://www.kankanews.com/list/xinwen/513"]
    for i in urls:
        url = i
        response = requests.get(url, headers=headers.header())
        response.encoding = "utf-8"
        if response.status_code == 200:
            html = response.text
            mistake = getURL(html)
            if mistake:
                break
        else:
            break


if __name__ == '__main__':
    starts()