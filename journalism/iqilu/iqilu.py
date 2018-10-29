import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.iqilu.news",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "齐鲁网",
    }
    print(dicts)
    # storageDatabase(dicts)



def download(html, number, title):
    pattern = re.compile('\d+-\d+-\d+ \d+:\d+:\d+')
    timeout = re.findall(pattern, html)[0]
    pattern = re.compile('<div class="clear"></div>[\s\S]*?二维码')
    format_text = re.findall(pattern, html)[0]
    format_text = re.sub('<div[\s\S]*?>', " ", format_text)
    format_text = re.sub('</div>', " ", format_text)
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
    pattern = re.compile('<!-- 齐鲁原创 -->[\s\S]*?<!-- 分页 -->')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<h3>[\s\S]*?</h3>')
    msg = re.findall(pattern, data)
    for message in msg:
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, message)
        url = text [0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.iqilu.news"):
        #     return True
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return True


def starts():
    urls = ["http://news.iqilu.com/shandong/yuanchuang/list_564_%s.shtml"]
    for i in urls:
        n = 1
        while True:
            url = i %n
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