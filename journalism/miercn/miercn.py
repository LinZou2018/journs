import re
import json
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.miercn.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout, exist=True),
        "format_text": format_text,
        "source": "米尔网",
    }
    print(dicts)
    # storageDatabase(dicts)


def getText(url, i):
    substitute = "_" + str(i) + ".html"
    url = re.sub(".html", substitute, url)
    response = requests.get(url, headers=headers.header())
    response.encoding = "gbk"
    if response.status_code == 200:
        html = response.text
        pattern = re.compile('(id="J-contain_detail_cnt"[\s\S]*?>)([\s\S]*?)(\s</div>)')
        format_text = re.findall(pattern, html)[0][1]
        pattern = re.compile('<p>[\s\S]*?</p>')
        exist = re.findall(pattern, format_text)
        if not exist:
            return
        return format_text


def download(html, number, url):
    print("1111")
    pattern = re.compile('(id="J-contain_detail_cnt"[\s\S]*?>)([\s\S]*?)(\s</div)')
    format_text = re.findall(pattern, html)[0][1]
    print(format_text)
    pattern = re.compile('<p>[\s\S]*?</p>')
    exist = re.findall(pattern, format_text)
    if not exist:
        return
    pattern = re.compile('来源：')
    exist = re.findall(pattern, html)
    if exist:
        return
    print("2222")
    pattern = re.compile('<div class="pagination">[\s\S]*?</div>')
    page = re.findall(pattern, html)[0]
    pattern = re.compile('(<a[\s\S]*?>)(\d+)(</a>)')
    page_num = re.findall(pattern, page)
    if page_num:
        for i in range(len(page_num) + 1):
            if i > 1:
                data = getText(url, i)
                format_text += data
    format_text = re.sub('<script>[\s\S]*?</script>', " ", format_text)
    format_text = re.sub('</div>', " ", format_text)
    format_text = re.sub('<style>[\s\S]*?</style>', " ", format_text)
    pattern = re.compile('(<h1><span>)([\s\S]*?)(</span></h1>)')
    title = re.findall(pattern, html)[0][1]
    pattern = re.compile('\d+-\d+-\d+ \d+:\d+')
    timeout = re.findall(pattern, html)[0]
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
        number = int(re.findall(pattern, url)[-2])
        # if rechecking(number, source_url="com.miercn.www"):
        #     return True
        mistake = connect(url, number)
        if mistake:
            return True


def starts():
    urls = ["http://www.miercn.com/zbs/getDatawaidinew?type=428&page=%s",
            "ttp://www.miercn.com/zbs/getDatawaidinew?type=7&page=%s",
            "http://www.miercn.com/zbs/getDatawaidinew?type=1&page=%s",
            "http://www.miercn.com/zbs/getDatawaidinew?type=4&page=%s",
            "http://www.miercn.com/zbs/getDatawaidinew?type=5&page=%s",
            "http://www.miercn.com/zbs/getDatawaidinew?type=3&page=%s"]
    for i in urls:
        n = 1
        while True:
            url = i % n
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