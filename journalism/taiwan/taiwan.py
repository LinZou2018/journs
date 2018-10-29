import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "cn.taiwan.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "中国台湾网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+年\d+月\d+日 \d+:\d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    print(exist)
    if not exist:
        return
    pattern = re.compile('中国台湾网')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    timestmap = time.strptime(timeout , "%Y年%m月%d日 %H:%M:%S")
    timeout = time.strftime("%Y-%m-%d %H:%M:%S", timestmap)
    pattern = re.compile('(<div class=TRS_Editor>)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, timeout, format_text)


def connect(url, number, title):
    response = requests.get(url, headers=headers.header())
    response.encoding = "gbk"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<ul class="list">[\s\S]*?</ul>')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<h2>[\s\S]*?</h2>')
    msg = re.findall(pattern, data)
    for message in msg:
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="cn.taiwan.www"):
        #     return True
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    urls = ["http://www.taiwan.cn/taiwan/index.htm", "http://www.taiwan.cn/plzhx/index.htm",
            "http://www.taiwan.cn/lilunpindao/index.htm", "http://www.taiwan.cn/xwzx/la/index.htm",
            "http://www.taiwan.cn/xwzx/index.htm", "http://culture.taiwan.cn/index.htm"]
    for i in urls:
        n = 0
        while True:
            if n == 0:
                url = i
            else:
                page = "_" + str(n) + ".htm"
                url = re.sub(".htm", page, i)
            response = requests.get(url, headers=headers.header())
            response.encoding = "gbk"
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