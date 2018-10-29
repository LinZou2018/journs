import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.china.news",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "中华网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)[0]
    pattern = re.compile('中华网')
    source = re.findall(pattern, exist[1])
    if not source:
        return
    timeout = exist[0]
    pattern = re.compile('(<div id="chan_newsDetail">)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, timeout, format_text)



def connect(url, number, title):
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = reponse.text
        download(html, number, title)


def getURL(html):
    pattern = re.compile('<ul>[\s\S]*?</ul>')
    differend = re.findall(pattern, html)
    for data in differend:
        pattern = re.compile('<li>[\s\S]*?</li>')
        msg = re.findall(pattern, data)
        for message in msg:
            pattern = re.compile('(href=")([\s\S]*?)(")')
            url = re.findall(pattern, message)[0][1]
            pattern = re.compile('\d+')
            number = int(re.findall(pattern, url)[-1])
            # if rechecking(number, source_url="com.china.news"):
            #     return True
            pattern = re.compile('(<a[\s\S]*？>)([\s\S]*?)(</a>)')
            title = re.findall(pattern, message)[0][1]
            connect(url, number, title)


def starts():
    urls = ["https://news.china.com/zh_cn/domestic/index.html", "https://news.china.com/zh_cn/international/index.html",
            "https://news.china.com/zh_cn/social/index.html", "https://news.china.com/zh_cn/focus/index.html",]
    for i in urls:
        url = i
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = reponse.text
            getURL(html)


if __name__ == '__main__':
    starts()