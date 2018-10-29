import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.yulefm.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "娱乐广播网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+)([\s\S]*?</span>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('娱乐广播')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    pattern = re.compile('<div id="content-body"[\s\S]*?</div>')
    text = re.findall(pattern, html)[0]
    pattern = re.compile('(<td>)([\s\S]*?)(</td>)')
    format_text = re.findall(pattern, text)[0][1]
    storage(number, title, timeout, format_text)


def connect(url, number, title):
    url = "http://www.yulefm.com" + url
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<!--/list-item-->[\s\S]*?<!--/list-item-->')
    data = re.findall(pattern, html)
    for message in data:
        pattern = re.compile('<h2>[\s\S]*?</h2>')
        msg = re.findall(pattern, message)[0]
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, msg)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.yule.www"):
        #     return True
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    urls = ["http://www.yulefm.com/star/index.html", "http://www.yulefm.com/movie/index.html",
            "http://www.yulefm.com/v/index.html", "http://www.yulefm.com/music/index.html",
            "http://www.yulefm.com/shishang/index.html"]
    for i in urls:
        n = 1
        while True:
            if n == 1:
                url = i
            else:
                page = "_" + str(n) + ".html"
                url = re.sub(".html", page, n)
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