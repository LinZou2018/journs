import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, author, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.nbd.www",
        "newsType": "news",
        "title": title,
        "author": author,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "每经网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number):
    pattern = re.compile('(<p class="u-time">[\s\S]*?)(\d+-\d+-\d+ \d+:\d+:\d+)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('每日经济新闻')
    source = re.findall(pattern, exist[0][0])
    if not source:
        return
    timeout = exist[0][1]
    pattern = re.compile('(<h1>[\s\S]*?-->)([\s\S]*?)(</h1>)')
    title = re.findall(pattern, html)[0][1]
    pattern = re.compile('(<div class="g-articl-text">)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
    pattern = re.compile('(<div class="u-editor">[\s\S]*?<span>)([\s\S]*?)(</span>[\s\S]*?</div>)')
    author = re.findall(pattern, html)
    if author:
        author = author[0][1]
    else:
        author = ""
    storage(number, title, author, timeout, format_text)


def connect(url, number):
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number)
    else:
        return


def getURL(html):
    pattern = re.compile('<div class="g-columnnews">[\s\S]*?</ul>')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<li>[\s\S]*?</li>')
    collection = re.findall(pattern, data)
    for message in collection:
        pattern= re.compile('<a[\s\S]*?</a>')
        text_url = re.findall(pattern, message)[1]
        pattern = re.compile('(href=")([\s\S]*?)(")')
        url = re.findall(pattern, text_url)[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.nbd.www"):
        #     return True
        mistake = connect(url, number)
        if mistake:
            return True


def starts():
    urls = ["http://economy.nbd.com.cn/", "http://industry.nbd.com.cn/", "http://stocks.nbd.com.cn/",
            "http://money.nbd.com.cn/", "http://www.nbd.com.cn/fangchan", "http://tmt.nbd.com.cn/",
            "http://world.nbd.com.cn/", "http://fxcj.nbd.com.cn/"]
    for url in urls:
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