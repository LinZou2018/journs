import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.chinanews.channel",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "中国新闻网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number):
    pattern = re.compile('<div  id="con">[\s\S]*?<!--分享-->')
    data = re.findall(pattern, html)
    if data:
        data = data[0]
    else:
        return
    pattern = re.compile('来源：[\s\S]*?</a>')
    source = re.findall(pattern, data)[1]
    pattern = re.compile('中国新闻网')
    exist = re.findall(pattern, source)
    if not exist:
        return
    pattern = re.compile('\d+-\d+-\d+ \d+:\d+:\d+')
    timeout = re.findall(pattern, data)[0]
    pattern = re.compile('(<h1[\s\S]*?>)([\s\S]*?)(</h1>)')
    title = re.findall(pattern, data)[0][1]
    pattern = re.compile('(<div class="left_zw"[\s\S]*?>)([\s\S]*?)(<div id="function_code_page">)')
    format_text = re.findall(pattern, data)[0][1]
    storage(number, title, timeout, format_text)


def connect(url, number):
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "gbk"
    if reponse.status_code == 200:
        html = reponse.text
        download(html, number)
    else:
        return True


def getURL(html):
    pattern = re.compile('<ul>[\s\S]*?</ul>')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<li>[\s\S]*?</li>')
    msg = re.findall(pattern, data)
    for message in msg:
        print(message)
        pattern = re.compile('(href=")([\s\S]*?)(")')
        urls = re.findall(pattern, message)
        if len(urls) == 1:
            url = "http:" + urls[0][1]
        else:
            url = "http:" + urls[1][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[3])
        # if rechecking(number, source_url="com.chinanews.channel"):
        #     return True
        data = connect(url, number)
        if data:
            return  True


def starts():
    urls = ["http://www.chinanews.com/scroll-news/news%s.html",
            "http://www.chinanews.com/mil/news.shtml"]
    n = 1
    for i in urls:
        if n == 1:
            while True:
                url = i % n
                reponse = requests.get(url, headers=headers.header())
                reponse.encoding = "gbk"
                if reponse.status_code == 200:
                    html = reponse.text
                    msg = getURL(html)
                    if msg:
                        break
                    n += 1
                else:
                    break
        else:
            url = i
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "gbk"
            if reponse.status_code == 200:
                html = reponse.text
                getURL(html)


if __name__ == '__main__':
    starts()