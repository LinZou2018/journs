import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.qinbaol.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "秦巴娱乐",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    print(html)
    pattern = re.compile('\d+-\d+-\d+ \d+:\d+:\d+')
    timeout = re.findall(pattern, html)[0]
    print(timeout)
    pattern = re.compile('(<div id="icontent">[\s\S]*?</div>)')
    format_text = re.findall(pattern, html)[0]
    pattern = re.compile('(<td>)([\s\S]*?)(</tr>)')
    format_text = re.findall(pattern, format_text)[0][1]
    storage(number, title, timeout, format_text)


def connect(url, number, title):
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<dd>[\s\S]*?</dd>')
    data = re.findall(pattern, html)
    for message in data:
        print(message)
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, message)
        if not text:
            continue
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.qinbaol.www"):
        #     return True
        title = text[0][-2]
        mistaek = connect(url, number, title)
        if mistaek:
            return True


def starts():
    n = 1
    while True:
        if n == 1:
            url = "https://www.qinbaol.com/ent/index.html"
        else:
            url = "https://www.qinbaol.com/ent/index_" + str(n) + ".html"
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