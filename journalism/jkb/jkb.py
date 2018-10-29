import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.enorth.news",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "北方网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+)([\s\S]*?</div> )')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('健康报')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    pattern = re.compile('(<div id="nc_con">)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, timeout, format_text)



def connect(url, number, title):
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)


def getURL(html):
    pattern = re.compile('<ul>[\s\S]*?</ul>')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<li[\s\S]*?</li>')
    msg = re.findall(pattern, data)
    for message in msg:
        pattern = re.compile('(<a href=")([\s\S]*?)("[\s\S]*?title=")([\s\S]*?)(">)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.jkb.www"):
        #     return True
        title = text[0][-2]
        connect(url, number,title)


def starts():
    urls = ["http://www.jkb.com.cn/news/industryNews/", "http://www.jkb.com.cn/news/technology/",
            "http://www.jkb.com.cn/news/healthCareReform/", "http://www.jkb.com.cn/news/dynamicSenior/",
            "http://www.jkb.com.cn/news/familyPlanning/", "http://www.jkb.com.cn/news/publicHealth/",
            "http://www.jkb.com.cn/news/depth/", "http://www.jkb.com.cn/news/commentary/",
            "http://www.jkb.com.cn/news/character/", "http://www.jkb.com.cn/news/overseas/"]
    for i in urls:
        url = i
        response = requests.get(url, headers=headers.header())
        response.encoding = "utf-8"
        if response.status_code == 200:
            html = response.text
            getURL(html)


if __name__ == '__main__':
    starts()