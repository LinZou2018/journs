import re
import json
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, message, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.chinanews.channel",
        "newsType": "news",
        "title": message["title"],
        "release_time": message["pubtime"],
        "create_time": seconds(message["pubtime"], exist=True),
        "format_text": format_text,
        "source": "中国新闻网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, message, number):
    pattern = re.compile('<div  id="con">[\s\S]*?<!--分享-->')
    data = re.findall(pattern, html)
    if data:
        data = data[0]
    else:
        return
    pattern = re.compile('来源：[\s\S]*?</a>')
    source = re.findall(pattern, data)[1]
    pattern = re.compile('中国新闻网')
    exist = re.findall(pattern, source)
    if not exist:
        return
    pattern = re.compile('(<div class="left_zw"[\s\S]*?>)([\s\S]*?)(<div id="function_code_page">)')
    format_text = re.findall(pattern, data)[0][1]
    storage(number, message, format_text)


def connect(url, message, number):
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "gbk"
    if reponse.status_code == 200:
        html = reponse.text
        download(html, message, number)
    else:
        return True


def getURL(html):
    pattern = re.compile('{[\s\S]*}')
    data = re.findall(pattern, html)[0]
    data = json.loads(data)
    docs = data["docs"]
    for message in docs:
        num = message["id"]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, num)[2])
        # if rechecking(number, source_url="com.chinanews.channel"):
        #     return True
        url = message["url"]
        msg = connect(url, message, number)
        if msg:
            return  True


def starts():
    urls = ["http://channel.chinanews.com/cns/s/channel:gn.shtml?pager=%s&pagenum=20&_=1538967821012",
            "http://channel.chinanews.com/cns/s/channel:gj.shtml?pager=%s&pagenum=20&_=1538967926509",
            "http://channel.chinanews.com/cns/s/channel:sh.shtml?pager=%s&pagenum=20&_=1538966862855",
            "http://channel.chinanews.com/cns/s/channel:cj.shtml?pager=%s&pagenum=20&_=1538966909525",
            "http://channel.chinanews.com/cns/s/channel:fortune.shtml?pager=%s&pagenum=8&_=1538967005401",
            "http://channel.chinanews.com/cns/s/channel:yl.shtml?pager=%s&pagenum=9&_=1538967034415",
            "http://channel.chinanews.com/cns/s/channel:ty.shtml?pager=%s&pagenum=7&_=1538967084379",
            "http://channel.chinanews.com/cns/s/channel:ll.shtml?pager=%s&pagenum=5&_=1538967127541"]
    for i in urls:
        n = 0
        while True:
            url = i % n
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            if reponse.status_code == 200:
                html = reponse.text
                msg = getURL(html)
                if msg:
                    break
                n += 1
                if  n > 3:
                    break


if __name__ == '__main__':
    starts()