import re
import json
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


headerll = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "0",
    "Host": "www.qianyan001.com",
    "Origin": "http://www.qianyan001.com",
    "Referer": "http://www.qianyan001.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.qianyan001.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout, exist=True),
        "format_text": format_text,
        "source": "前沿网",
    }
    print(dicts)
    # storageDatabase(dicts)


def getText(url, number, i):
    substitute = str(number) + "_" + str(i)
    url = re.sub(str(number), substitute, url)
    response = requests.get(url, headers=headers.header())
    response.encoding = "gbk"
    if response.status_code == 200:
        html = response.text
        pattern = re.compile('(id="J-contain_detail_cnt"[\s\S]*?>)([\s\S]*?)(<div class="gg_item_bomttom_cnt" >)')
        format_text = re.findall(pattern, html)[0][1]
        pattern = re.compile('<p>[\s\S]*?</p>')
        exist = re.findall(pattern, format_text)
        if not exist:
            return
        format_text = re.sub('<script>[\s\S]*></script>', " ", format_text)
        format_text = re.sub('</div>', " ", format_text)
        return format_text


def download(html, number, url):
    pattern = re.compile('(id="J-contain_detail_cnt"[\s\S]*?>)([\s\S]*?)(<div class="gg_item_bomttom_cnt" >)')
    format_text = re.findall(pattern, html)[0][1]
    pattern = re.compile('<p>[\s\S]*?</p>')
    exist = re.findall(pattern, format_text)
    if not exist:
        return
    format_text = re.sub('<script>[\s\S]*></script>', " ", format_text)
    format_text = re.sub('</div>', " ", format_text)
    pattern = re.compile('(<title>)([\s\S]*?)(</title>)')
    title = re.findall(pattern, html)[0][1]
    pattern = re.compile('前沿网')
    exist = re.findall(pattern, title)
    if not exist:
        return
    pattern = re.compile('\d+-\d+-\d+ \d+:\d+')
    timeout = re.findall(pattern, html)[0]
    pattern = re.compile('<div class="pagination">[\s\S]*?</div>')
    page = re.findall(pattern, html)[0]
    pattern = re.compile('(<a[\s\S]*?>)(\d+)(</a>)')
    page_num = re.findall(pattern, page)
    if page_num:
        for i in range(len(page_num) + 1):
            if i > 1:
                data = getText(url, number, i)
                format_text += data
    storage(number, title, timeout, format_text)


def connect(url, number):
    response = requests.get(url, headers=headers.header())
    response.encoding = "gbk"
    if response.status_code == 200:
        html = response.text
        download(html, number, url)
    else:
        return True


def getURL(html):
    data = json.loads(html)
    text_list = data["list"]
    for message in text_list:
        url = message["url"]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="com.qianyan001.www"):
        #     return True
        mistake = connect(url, number)
        if mistake:
            return True


def starts():
    urls = ["http://www.qianyan001.com/zbs/getData?type=428&page=%s",
            "http://www.qianyan001.com/zbs/getData?type=255&page=%s",
            "http://www.qianyan001.com/zbs/getData?type=243&page=%s",
            "http://www.qianyan001.com/zbs/getData?type=237&page=%s",
            "http://www.qianyan001.com/zbs/getData?type=456&page=%s"]
    for i in urls:
        n = 1
        while True:
            url = i % n
            response = requests.post(url, headers=headerll)
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