import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.caijing.finance",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "财经网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('\d+-\d+-\d+ \d+:\d+:\d+')
    timeout = re.findall(pattern, html)
    if timeout:
        timeout = timeout[0]
    else:
        pattern = re.compile('\d{4}/\d{2}/\d{2}')
        timeout = re.findall(pattern, html)
        if timeout:
            timeout = timeout[0] + " 09:00:00"
            timeArray = time.strptime(timeout, "%Y/%m/%d %H:%M:%S")
            timeout = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        else:
            pattern = re.compile('\d+-\d+-\d+ \d+:\d+')
            timeout = re.findall(pattern, html)[0] + ":00"
    pattern = re.compile('(<div id="the_content"[\s\S]*?>[\s\S]*?)(<style>)')
    format_text = re.findall(pattern, html)
    if format_text:
        format_text = format_text[0][0]
    else:
        pattern = re.compile('(<div class="article-content">)([\s\S]*?)(</div>)')
        format_text = re.findall(pattern, html)[0][1]
    format_text = re.sub('<div[\s\S]*?>', '<div>', format_text)
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
    pattern = re.compile('<ul class="list">[\s\S]*?</ul>')
    msg = re.findall(pattern, html)[0]
    pattern = re.compile('<li>[\s\S]*?</li>')
    data = re.findall(pattern, msg)
    for message in data:
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.caijing.finance"):
        #     return True
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    urls = "http://yuanchuang.caijing.com.cn/%s.shtml"
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