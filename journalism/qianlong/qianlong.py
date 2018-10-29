import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, author, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.qianlong.news",
        "newsType": "news",
        "title": title,
        "author": author,
        "release_time": timeout,
        "create_time": seconds(timeout, exist=True),
        "format_text": format_text,
        "source": "千龙网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('\d+-\d+-\d+\s*?\d+:\d+')
    timeout = re.findall(pattern, html)[0].split()
    timeout = timeout[0] + " " + timeout[1]
    pattern = re.compile('(<div class="article-content">)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)
    if format_text:
        format_text = format_text[0][1]
    else:
        pattern = re.compile('(<div id="lm1">)([\s\S]*?)(</div>)')
        format_text = re.findall(pattern, html)[0][1]
    pattern = re.compile('<p class="editor">[\s\S]*?</p>')
    authors = re.findall(pattern, html)
    if len(authors) == 2:
        author = authors[1][1]
    else:
        author = ""
    storage(number, title, author, timeout, format_text)


def connect(url, number, title):
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = reponse.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<ul class="media-list list6">[\s\S]*?</ul>')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<li>[\s\S]*?</li>')
    msg = re.findall(pattern, data)
    for message in msg:
        pattern = re.compile('(href=")([\s\S]*?)(")')
        url = re.findall(pattern, message)[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[2])
        # if rechecking(number, source_url="com.qianlong.news"):
        #     return True
        pattern = re.compile('(title=")([\s\S]*?)(")')
        title = re.findall(pattern, message)[0][1]
        data = connect(url, number, title)
        if data:
            return True


def starts():
    urls = ["http://news.qianlong.com/qlyc/qlcf1/index%s.shtml", "http://news.qianlong.com/qlyc/qlpl1/index%s.shtml",
            "http://news.qianlong.com/qlyc/qltx1/index%s.shtml", "http://news.qianlong.com/qlyc/qlsp1/index%s.shtml",
            "http://news.qianlong.com/qlyc/qlsz1/index%s.shtml", "http://news.qianlong.com/qlyc/qlyl1/index%s.shtml",
            "http://news.qianlong.com/qlyc/qlwh1/index%s.shtml", "http://news.qianlong.com/qlyc/qlzx1/index%s.shtml",
            "http://news.qianlong.com/qlyc/qljy1/index%s.shtml", "http://news.qianlong.com/qlyc/qlzk1/index%s.shtml"]
    for i in urls:
        n = 0
        while True:
            if n >= 1:
                url = i % ("_" + str(n))
            else:
                url = i % ""
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            if reponse.status_code == 200:
                html = reponse.text
                data = getURL(html)
                if data:
                    break
            else:
                break


if __name__ == '__main__':
    starts()