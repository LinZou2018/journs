import re
import json
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(message, format_text):
    dicts = {
        "source_id": int(message["DocID"]),
        "source_url": "com.xinhuanet.www",
        "newsType": "news",
        "title": message["Title"],
        "author": message["Author"],
        "release_time": message["PubTime"],
        "create_time": seconds(message["PubTime"]),
        "format_text": format_text,
        "source": "新华网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, message):
    pattern = re.compile('(<span>[\s\S]*?来源：[\s\S]*?</span>)')
    source = re.findall(pattern, html)
    if not source:
        return
    source = source[0]
    pattern = re.compile('新华网')
    exist = re.findall(pattern, source)
    if not exist:
        return
    pattern = re.compile('<div class="main">[\s\S]*?<div class="seo"')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<div id="p-detail">[\s\S]*?<div class="zan-wap">')
    text = re.findall(pattern, data)[0]
    pattern = re.compile('<p[\s\S]*?>[\s\S]*</p>')
    format_text = re.findall(pattern, text)[0]
    storage(message, format_text)


def createLinks(url, message):
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = reponse.text
        download(html, message)


def getURL(html):
    pattern = re.compile("{[\s\S]*}")
    dicts = re.findall(pattern, html)[0]
    data = json.loads(dicts)
    data = data["data"]
    data_list = data["list"]
    for message in data_list:
        number = int(message["DocID"])
        # if rechecking(number, source_url="com.xinhuanet.www"):
        #     return
        url = message["LinkUrl"]
        createLinks(url, message)


def starts():
    urls = ["http://qc.wa.news.cn/nodeart/list?nid=113352&pgnum=1&cnt=10&tp=1&orderby=1?callback=jQuery11240060845457767172206_1538277291539&_=1538277291540",
            "http://qc.wa.news.cn/nodeart/list?nid=11147664&pgnum=1&cnt=16&tp=1&orderby=1?callback=jQuery17107865590976021672_1538278999787&_=1538279000034",
            "http://qc.wa.news.cn/nodeart/list?nid=116713&pgnum=1&cnt=10&tp=1&orderby=1?callback=jQuery171014948965342051235_1538279083028&_=1538279083302",
            "http://qc.wa.news.cn/nodeart/list?nid=11109063&pgnum=1&cnt=10&tp=1&orderby=1?callback=jQuery112409549135277360858_1538279369067&_=1538279369068"]
    for i in urls:
        url = i
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = reponse.text
            getURL(html)


if __name__ == '__main__':
    starts()