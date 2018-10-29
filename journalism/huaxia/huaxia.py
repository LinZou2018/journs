import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.huaxia.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "华夏经纬网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(class="style">[\s\S]*?)(\d+-\d+-\d+ \d+:\d+:\d+)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('华夏经纬网')
    source = re.findall(pattern, exist[0][0])
    if not source:
        return
    timeout = exist[0][1]
    pattern = re.compile('(<td[\s\S]*?id="oImg">)([\s\S]*?)(</td>)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, timeout, format_text)


def connect(url, number, title):
    url = "http://www.huaxia.com" + url
    response = requests.get(url, headers=headers.header())
    response.encoding = "gbk"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<TABLE border=0 cellSpacing=0 cellPadding=0 width="100%" \s+height=20>[\s\S]*?</TABLE>')
    data = re.findall(pattern, html)
    for message in data:
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</A>)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.huaxia.www"):
        #     return True
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    urls = ["http://www.huaxia.com/xw/dlxw/index.html", "http://www.huaxia.com/xw/twxw/index.html",
            "http://www.huaxia.com/xw/gaxw/index.html", "http://www.huaxia.com/xw/gjxw/index.html",
            "http://www.huaxia.com/xw/zhxw/index.html"]
    for i in urls:
        n = 1
        while True:
            if n == 1:
                url = i
            else:
                page = "_" + str(n) + ".html"
                url = re.sub(".html", page, i)
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