import re
import json
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, author, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.163.news",
        "newsType": "news",
        "title": title,
        "author": author,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "网易新闻",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, message, number):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+)([\s\S]*?</a>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    source = exist[0][1]
    pattern = re.compile('href="#"')
    source_url = re.findall(pattern, source)
    if not source_url:
        return
    timeout = exist[0][0]
    pattern = re.compile('(<div class="post_text" id="endText"[\s\S]*?>)([\s\S]*?)(<p><!--)')
    format_text = re.findall(pattern, html)[0][1]
    title = message["title"]
    pattern = re.compile('(<a[\s\S]*?>)([\s\S]*?)(</a>)')
    author = re.findall(pattern, source)[0][1]
    storage(number, title, author, timeout, format_text)


def connect(url, message, number):
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "gbk"
    if reponse.status_code == 200:
        html = reponse.text
        download(html, message, number)
    else:
        return True


def getURL(html):
    pattern = re.compile('\[[\s\S]*\]')
    data = re.findall(pattern, html)[0]
    data = json.loads(data)
    for message in data:
        url = message["docurl"]
        pattern = re.compile('(/)([a-z0-9A-Z]*?)(.html)')
        number = re.findall(pattern, url)[0][1]
        # if rechecking(number, source_url="com.163.news"):
        #     return True
        msg = connect(url, message, number)
        if msg:
            return


def starts():
    urls = ["https://temp.163.com/special/00804KVA/cm_yaowen.js?callback=data_callback",
            "https://temp.163.com/special/00804KVA/cm_guonei.js?callback=data_callback",
            "ttps://temp.163.com/special/00804KVA/cm_guoji.js?callback=data_callback",
            "https://temp.163.com/special/00804KVA/cm_dujia.js?callback=data_callback",
            "https://temp.163.com/special/00804KVA/cm_war.js?callback=data_callback",
            "https://temp.163.com/special/00804KVA/cm_money.js?callback=data_callback",
            "https://temp.163.com/special/00804KVA/cm_tech.js?callback=data_callback",
            "https://temp.163.com/special/00804KVA/cm_ent.js?callback=data_callback",
            "https://temp.163.com/special/00804KVA/cm_sports.js?callback=data_callback",
            "https://temp.163.com/special/00804KVA/cm_jiankang.js?callback=data_callback",
            "https://temp.163.com/special/00804KVA/cm_hangkong.js?callback=data_callback"]
    for i in urls:
        url = i
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "gbk"
        if reponse.status_code == 200:
            html = reponse.text
            getURL(html)


if __name__ == '__main__':
    starts()