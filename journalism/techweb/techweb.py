import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, author, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.techweb.www",
        "newsType": "news",
        "title": title,
        "author": author,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "TechWeb",
    }
    print(dicts)
    # storageDatabase(dicts)



def download(html, number, title):
    pattern = re.compile('(\d+.\d+.\d+ \d+:\d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)[0]
    timeout = exist[0]
    timestmap = time.strptime(timeout, "%Y.%m.%d %H:%M:%S")
    timeout = time.strftime("%Y-%m-%d %H:%M:%S", timestmap)
    pattern = re.compile('(作者:)([\s\S]*?)(</span>)')
    author = re.findall(pattern, exist[1])[0][1]
    pattern = re.compile('(<div id="content">)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)
    storage(number, title, author, timeout, format_text)


def connect(url, number, title):
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<div class="list_con">[\s\S]*?末页')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('(<div class="text">[\s\S]*?><h4>)([\s\S]*?)(</h4></a>)')
    text_list = re.findall(pattern, data)
    for message in text_list:
        pattern = re.compile('(href=")([\s\S]*?)(")')
        url = re.findall(pattern, message[0])[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.techweb.www"):
        #     return True
        title = message[1]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    urls = "http://www.techweb.com.cn/yuanchuang/list_%s.shtml#wp"
    n = 1
    while True:
        url = urls % n
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