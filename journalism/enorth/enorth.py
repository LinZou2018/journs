import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, author, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.enorth.news",
        "newsType": "news",
        "title": title,
        "authoe": author,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "北方网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(来源：[\s\S]*?)(\d+-\d+-\d+ \d+:\d+:\d+)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('北方网')
    source = re.findall(pattern, exist[0][0])
    if not source:
        return
    timeout = exist[0][1]
    pattern = re.compile('(作者：)([\s\S]*?)(</span>)')
    author = re.findall(pattern, exist[0][0])[0][1]
    pattern = re.compile('(<div align="center">[\s\S]*?</div>)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, author, timeout, format_text)


def connect(url, number, title):
    response = requests.get(url, headers=headers.header())
    response.encoding = "gb2312"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return


def getURL(html):
    pattern = re.compile('<table width="100%" >[\s\S]*?</table>')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<tr>[\s\S]*?</tr>')
    text = re.findall(pattern, data)
    for message in text:
        pattern = re.compile('(<a class="zi14" href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        exist = re.findall(pattern, message)
        url = exist[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.enorth.news"):
        #     return True
        title = exist[0][-2]
        connect(url, number, title)


def starts():
    url = "http://news.enorth.com.cn/system/count/0017000/000000000000/count_page_list_0017000000000000000.js"
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        pattern = re.compile('(maxpage = )(8287)(;)')
        page = int(re.findall(pattern, html)[0][1])
    else:
        return
    n = 0
    while True:
        if n == 0:
            url = "http://news.enorth.com.cn/gd/"
        else:
            url = "http://news.enorth.com.cn/system/more/17000000000000000/0082/17000000000000000_0000%s.shtml" % page
        response = requests.get(url, headers=headers.header())
        response.encoding = "gb2312"
        if response.status_code == 200:
            html = response.text
            mistake = getURL(html)
            if mistake:
                break
            page -= n
            n += 1
        else:
            break


if __name__ == '__main__':
    starts()