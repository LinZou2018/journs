import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "cn.guancha.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "观察者",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('观察')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    pattern = re.compile('(<div class="content all-txt">)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, timeout, format_text)


def connect(url, number, title):
    url = "https://www.guancha.cn" + url
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<ul class="column-list fix">[\s\S]*?</ul>')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<h4[\s\S]*?>[\s\S]*?</h4>')
    msg = re.findall(pattern, data)
    for message in msg:
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number= int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="cn.guancha.www"):
        #     return True
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    urls = ["https://www.guancha.cn/GongYe%C2%B7KeJi/list_", "https://www.guancha.cn/GuoJi%C2%B7ZhanLue/list_",
            "https://www.guancha.cn/JunShi/list_", "https://www.guancha.cn/ChanJing/list_",
            "https://www.guancha.cn/qiche/list_"]
    for i in urls:
        n = 1
        while True:
            url = i + str(n) + ".shtml"
            response = requests.get(url, headers=headers.header())
            response.encoding = "utf-8"
            if response.status_code == 200:
                html = response.text
                mistake =getURL(html)
                if mistake:
                    break
                n += 1
            else:
                break



if __name__ == '__main__':
    starts()