import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, author, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.ittime.www",
        "newsType": "news",
        "title": title,
        "author": author,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "IT时代网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('<p>来源：[\s\S]*?</p>')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('IT')
    source = re.findall(pattern, exist[0])
    if not source:
        return
    pattern = re.compile('(</h2>[\s\S]*?)(\d+年\d+月\d+日 \d+:\d+)')
    data = re.findall(pattern, html)
    timeout = data[0][1]
    timeArray = time.strptime(timeout + ":00", "%Y年%m月%d日 %H:%M:%S")
    timeout = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    pattern = re.compile('(<a[\s\S]*?>)([\s\S]*?)(</a>)')
    author = re.findall(pattern, data[0][0])[0][1]
    pattern = re.compile('(<div class="left_main">[\s\S]*?<style>)')
    text = re.findall(pattern, html)[0]
    pattern = re.compile('(\s</script>\s)([\s\S]*?)(<style>)')
    format_text = re.findall(pattern, text)[0][1]
    storage(number, title, author, timeout, format_text)


def connect(url, number, title):
    url = "https://www.ittime.com.cn" + url
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<dl class="newsList">[\s\S]*?</dl>')
    data = re.findall(pattern, html)
    for message in data:
        pattern = re.compile('(<h2><a href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a></h2>)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.ittime.www"):
        #     return True
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    urls = ["https://www.ittime.com.cn/news/chuangxin.shtml", "https://www.ittime.com.cn/chuangke.shtml",
            "https://www.ittime.com.cn/dujia.shtml", "https://www.ittime.com.cn/news/zixun.shtml"]
    for i in urls:
        n = 1
        while True:
            if n == 1:
                url = i
            else:
                pub = "_" + str(n) + ".shtml"
                url = re.sub(".shtml", pub, i)
            response = requests.get(url, headers=headers.header())
            response.encoding = "utf-8"
            if response.status_code == 200:
                html = response.text
                mistake = getURL(html)
                if mistake:
                    break
                n += 1
            else:
                break


if __name__ == '__main__':
    starts()