import re
import time
import json
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


headerll = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "7",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "www.tvoao.com",
    "Origin": "http://www.tvoao.com",
    "Referer": "http://www.tvoao.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def storage(message, format_text):
    dicts = {
        "source_id": int(message["articleid"]),
        "source_url": "com.tvoao.www",
        "newsType": "news",
        "title": message["title"],
        "release_time": message["showtime"],
        "create_time": seconds(message["showtime"]),
        "format_text": format_text,
        "source": "中广互联",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, message):
    pattern = re.compile('(\d+年\d+月\d+日)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('中广')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    pattern = re.compile('(<div class="text_content">)([\s\S]*?)(<!--已投票-->)')
    format_text = re.findall(pattern, html)[0][1]
    format_text = re.sub('<div[\s\S]*?>', "", format_text)
    format_text = re.sub('</div>', "", format_text)
    storage(message, format_text)



def connect(message):
    url = "http://www.tvoao.com/a/" + message["articleid"] +".aspx"
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, message)
    else:
        return True


def getURL(html):
    data = json.loads(html)
    for message in data:
        number = message["articleid"]
        # if rechecking(number, source_url="com.tvoao.www"):
        #     return True
        mistake = connect(message)
        if mistake:
            return True


def starts():
    n = 0
    url = "http://www.tvoao.com/Index/bidu_list"
    while True:
        data = {
            "limit": n,
        }
        response = requests.post(url, data=data, headers=headerll)
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
