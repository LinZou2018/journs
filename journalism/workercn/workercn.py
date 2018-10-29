import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, timeout, format_text):
    dicts = {
        "source_id": number,
        "source_url": "com.workercn.www",
        "newsType": "news",
        "title": title,
        "release_time": timeout,
        "create_time": seconds(timeout),
        "format_text": format_text,
        "source": "中工网",
    }
    print(dicts)
    # storageDatabase(dicts)


def download(html, number, title):
    pattern = re.compile('(\d+-\d+-\d+ \d+:\d+:\d+)([\s\S]*?</div>)')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('中工网')
    source = re.findall(pattern, exist[0][1])
    if not source:
        return
    timeout = exist[0][0]
    pattern = re.compile('(<div class="ccontent">)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)[0][1]
    storage(number, title, timeout, format_text)


def connect(url, number, title):
    pattern = re.compile('http')
    exist = re.findall(pattern, url)
    if exist:
        url = url
    else:
        url = "http://news.workercn.cn" + url
    response = requests.get(url, headers=headers.header())
    response.encoding = "gbk"
    if response.status_code == 200:
        html = response.text
        download(html, number, title)
    else:
        return True


def getURL(html):
    pattern = re.compile('<ul class="imgtxt1">[\s\S]*?</ul>')
    data = re.findall(pattern, html)
    print(data)
    pattern = re.compile('<ul>[\s\S]*?</ul>')
    msg = re.findall(pattern, html)
    if data:
        text = data[0] + msg[1]
    else:
        text = msg[1]
    pattern = re.compile('<h3>[\s\S]*?</h3>')
    text_list = re.findall(pattern, text)
    for message in text_list:
        pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
        text = re.findall(pattern, message)
        url = text[0][1]
        pattern = re.compile('\d+')
        number = int(re.findall(pattern, url)[-1])
        # if rechecking(number, source_url="cn.workercn.www"):
        #     return
        title = text[0][-2]
        mistake = connect(url, number, title)
        if mistake:
            return


def starts():
    urls = ["http://news.workercn.cn/32839/32839.shtml", "http://news.workercn.cn/32841/32841.shtml",
            "http://news.workercn.cn/32842/32842.shtml", "http://news.workercn.cn/32843/32843.shtml",
            "http://news.workercn.cn/32844/32844.shtml", "http://finance.workercn.cn/33004/33004.shtml",
            "http://finance.workercn.cn/33006/33006.shtml", "http://finance.workercn.cn/33005/33005.shtml",
            "http://finance.workercn.cn/33007/33007.shtml", "http://world.workercn.cn/32829/32829.shtml",
            "http://world.workercn.cn/32830/32830.shtml", "http://world.workercn.cn/32831/32831.shtml",
            "http://world.workercn.cn/32832/32832.shtml", "http://world.workercn.cn/32834/32834.shtml",
            "http://world.workercn.cn/32833/32833.shtml", "http://military.workercn.cn/32817/32817.shtml",
            "http://military.workercn.cn/32819/32819.shtml", "http://military.workercn.cn/32820/32820.shtml",
            "http://military.workercn.cn/32821/32821.shtml", "http://military.workercn.cn/32822/32822.shtml",
            "http://military.workercn.cn/32823/32823.shtml", "http://ent.workercn.cn/30021/30021.shtml",
            "http://ent.workercn.cn/30020/30020.shtml", "http://ent.workercn.cn/30022/30022.shtml",
            "http://ent.workercn.cn/30023/30023.shtml", "http://ent.workercn.cn/30026/30026.shtml"]
    for i in urls:
        url = i
        response = requests.get(url, headers=headers.header())
        response.encoding = "gbk"
        if response.status_code == 200:
            html = response.text
            getURL(html)


if __name__ == '__main__':
    starts()