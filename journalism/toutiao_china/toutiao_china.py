"""未能发现其有原创新闻"""
import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def download(html, number, title):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)[0]
    pattern = re.compile('')


def connect(url, number, title):
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = reponse.text
        download(html, number, title)


def getURL(html):
    pattern = re.compile('<ul class="item_run">[\s\S]*?</ul>')
    data = re.findall(pattern, html)[0]
    pattern = re.compile('<li>[\s\S]*?</li>')
    msg = re.findall(pattern, data)
    for message in msg:
        pattern = re.compile('(href=")([\s\S]*?)(")')
        url = re.findall(pattern, message)
        if url:
            url = url[0][1]
        else:
            continue
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.china.toutiao"):
        #     return True
        pattern = re.compile('(<a[\s\S]*?>)([\s\S]*?)(</a>)')
        title = re.findall(pattern, message)[0][1]
        connect(url, number, title)


def starts():
    urls = ["https://toutiao.china.com/shsy/gundong/", "https://toutiao.china.com/jssy/gundong/",
            "https://toutiao.china.com/ylsy/gundong/", "https://toutiao.china.com/cjsy/gundong/",
            "https://toutiao.china.com/jksy/gundong/", "https://toutiao.china.com/qgsy/gundong/",
            "https://toutiao.china.com/nxwsy/gundong/", "https://toutiao.china.com/nrsy/gundong/"]
    for i in urls:
        url = i
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = reponse.text
            getURL(html)


if __name__ == '__main__':
    starts()