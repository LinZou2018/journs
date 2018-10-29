import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.hupu.voice",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "虎扑",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(来源：[\s\S]*?)(\d+-\d+-\d+ \d+:\d+:\d+)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('虎扑')
    source = re.findall(pattern, exist[0][0])
    if not source:
        return
    timeout = exist[0][1]
    pattern = re.compile('(一般全文 start -->)([\s\S]*?)(<!-- 一般全文 end)')
    format_text = re.findall(pattern, html)[0][1]
    format_text = re.sub("<div[\s\S]*?>", "<p>", format_text)
    format_text = re.sub("</div>", "</p>", format_text)
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
    pattern = re.compile('<ul>[\s\S]*?</ul>')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<h4>[\s\S]*?</h4>')
    msg = re.findall(pattern, data)
    for message in msg:
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.hupu.voice"):
        #     return True
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    urls = ["https://voice.hupu.com/nba/", "https://voice.hupu.com/cba/",
            "https://voice.hupu.com/china/", "https://voice.hupu.com/f1/",
            "https://voice.hupu.com/soccer/"]
    for i in urls:
        n = 1
        while True:
            url = i + str(n)
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