import re
import json
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(message, format_text):
    dicts = {
        "source_id": int(message["guid"]),
        "source_url": "cn.haiwainet.opa",
        "newsType": "news",
        "title": message["title"],
        "release_time": message["pubtime"],
        "create_time": seconds(message["pubtime"]),
        "format_text": format_text,
        "source": "海外网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, message):
    pattern = re.compile('\d+-\d+-\d+ \d+:\d+:\d+[\s\S]*?</div>')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('海外网')
    source = re.findall(pattern, exist[0])
    if not source:
        return
    pattern = re.compile('(<div class="c mlr20" id="cen">)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)
    if format_text:
        format_text = format_text[0][1]
    else:
        pattern = re.compile('(<div class="contentMain">)([\s\S]*?)(</div>)')
        format_text = re.findall(pattern, html)[0][1]
    format_text = re.sub('<div[\s\S]*?>', " ", format_text)
    format_text = re.sub('</div>', " ", format_text)
    storage(message, format_text)


def connect(message):
    url = message["link"]
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, message)
    else:
        return True


def getURL(html):
    data = json.loads(html)
    msg = data["result"]
    for message in msg:
        number = int(message["guid"])
        # if rechecking(number, source_url="cn.haiwainet.opa"):
        #     return True
        mistake = connect(message)
        if mistake:
            return True


def starts():
    n = 1
    while True:
        url = "http://opa.haiwainet.cn/apis/news?catid=3541093&num=10&page=" + str(n)
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