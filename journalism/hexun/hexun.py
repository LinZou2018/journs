import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.163.news",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "和讯",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+)(</span>[\s\S]*?</a>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('和讯')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    pattern = re.compile('(<div class="art_contextBox"[\s\S]*?>)([\s\S]*?)(<div)')
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
    pattern = re.compile('{id[\s\S]*?}')
    data = re.findall(pattern, html)
    for message in data:
        pattern = re.compile("(id:')([\s\S]*?)(')")
        number = int(re.findall(pattern, message)[0][1])
        # if rechecking(number, source_url="com.hexun.roll"):
        #     return True
        pattern = re.compile("(title:')([\s\S]*?)(')")
        title = re.findall(pattern, message)[0][1]
        pattern = re.compile("(titleLink:')([\s\S]*?)(')")
        url = re.findall(pattern, message)[0][1]
        msg = connect(url, number, title)
        if msg:
            return True


def starts():
    differend = "http://roll.hexun.com/roolNews_listRool.action?type=all&ids=100,101,103,125,105,124,162,194,108,122,121,119,\
107,116,114,115,182,120,169,170,177,180,118,190,200,155,130,117,153,106&date=2018-10-10&page=%s"
    n = 1
    while True:
        url = differend % n
        reponse = requests.get(url, headers=headers.header())
        # reponse.content.decode('gbk','ignore')
        reponse.encoding = "gbk2312"
        if reponse.status_code == 200:
            html = reponse.text
            data = getURL(html)
            if data:
                break
            n += 1
        else:
            break


if __name__ == '__main__':
    starts()