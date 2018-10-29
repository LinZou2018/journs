import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "cn.hinews.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "海南网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(<div[\s\S]*?id="laiy">[\s\S]*?)(\d+-\d+-\d+ \d+:\d+:\d+)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('海南')
    source = re.findall(pattern, exist[0][0])
    if not source:
        return
    timeout = exist[0][1]
    pattern = re.compile('(<div id="zt">)([\s\S]*?)(</div>)')
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
    pattern = re.compile('<ul class="marh l25 f14 fl ml10 mr10"[\s\S]*?</ul>')
    data = re.findall(pattern, html)
    for dataOne in data:
        pattern = re.compile('<li>[\s\S]*?</li>')
        msg = re.findall(pattern, dataOne)
        for message in msg:
            pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
            text = re.findall(pattern, message)
            url = text[0][1]
            pattern = re.compile('\d+')
            number = int(re.findall(pattern, url)[-1])
            # if rechecking(number, source_url="cn.hinews.www"):
            #     return
            title = text[0][-2]
            mistake = connect(url, number, title)
            if mistake:
                return


def starts():
    urls = ["http://www.hinews.cn/news/guonei/", "http://www.hinews.cn/news/guoji/",
            "http://www.hinews.cn/news/shehui/", "http://www.hinews.cn/news/yule/",
            "http://www.hinews.cn/news/tiyu/"]
    for i in urls:
        url = i
        response = requests.get(url, headers=headers.header())
        response.encoding = "gbk"
        if response.status_code == 200:
            html = response.text
            getURL(html)


if __name__ == '__main__':
    starts()