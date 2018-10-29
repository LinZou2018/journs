import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.legaldaily.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout, exist=True),
        "format_text": format_text,
        "source": "法制网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+)([\s\S]*?来源[\s\S]*?</dd>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('法制')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    pattern = re.compile('(<dd[\s\S]*?class="f14 black02 yh">)([\s\S]*?)(</dd>)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, timeout, format_text)


def connect(url, number, title):
    response = requests.get(url, headers=headers.header())
    response.encoding ="utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<div id="div1000">[\s\S]*?</div>')
    data = re.findall(pattern, html)[1]
    pattern = re.compile('<a[\s\S]*?</a>')
    msg = re.findall(pattern, data)
    for message in msg:
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?</span>)([\s\S]*?)(<span)')
        text = re.findall(pattern, message)
        if not text:
            continue
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="utf-8"):
        #     return True
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    urls = ["http://www.legaldaily.com.cn/index_article/node_5955.htm",
            "http://www.legaldaily.com.cn/Finance_and_Economics/node_75684.htm",
            "http://www.legaldaily.com.cn/IT/node_69471.htm", "http://www.legaldaily.com.cn/society/node_55564.htm",
            "http://www.legaldaily.com.cn/army/node_80560.htm"]
    for i in urls:
        n = 1
        while True:
            if n == 1:
                url = i
            else:
                page = "_" + str(n) + ".htm"
                url = re.sub(".htm", page, i)
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
