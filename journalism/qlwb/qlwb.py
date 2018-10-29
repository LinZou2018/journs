import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.qlwb.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "齐鲁晚报",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, title, number):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('齐鲁')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    pattern = re.compile('(<div class="article-content fontSizeSmall BSHARE_POP">)([\s\S]*?)(<div)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, timeout, format_text)


def connect(url, title, number):
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, title, number)
    else:
        return True


def getURL(html):
    pattern = re.compile('<div class="h149">[\s\S]*?</div>')
    text = re.findall(pattern, html)
    for message in text:
        pattern = re.compile('<li[\s\S]*?>[\s\S]*?</li>')
        data = re.findall(pattern, message)[0]
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        msg = re.findall(pattern, data)[0]
        url = msg[1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.qlwb.www"):
        #     return True
        title = msg[-2]
        mistake = connect(url, title, number)
        if mistake:
            return True


def starts():
    urls = ["http://www.qlwb.com.cn/news/domesticnews/%s.shtml", "http://www.qlwb.com.cn/news/overseas/%s.shtml",
            "http://www.qlwb.com.cn/news/SocialNews/%s.shtml", "http://www.qlwb.com.cn/news/sports/%s.shtml",
            "http://www.qlwb.com.cn/news/importantnews/%s.shtml", "http://www.qlwb.com.cn/news/commentary/%s.shtml",
            "http://yule.qlwb.com.cn/"]
    for i in urls:
        n = 1
        while True:
            if i == "http://yule.qlwb.com.cn":
                url = i
            else:
                url = i % n
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