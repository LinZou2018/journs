import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def starts():
    pass


if __name__ == '__main__':
    starts()


# pattern = re.compile('(href=")([\s\S]*?)("[\s\S]*?>)([\s\S]*?)(</a>)')
# text = re.findall(pattern, message)
# url = text[0][1]
# pattern = re.compile('\d+')
# number = int(re.findall(pattern, url)[-1])
# # if rechecking(number, source_url="com.jiemian.www"):
# #     return
# title = text[0][-2]
# mistake = connect(url, number, title)
# if mistake:
#     return
#
#
# def connect(url, number, title):
#     response = requests.get(url, headers=headers.header())
#     response.encoding = "utf-8"
#     if response.status_code == 200:
#         html = response.text
#         download(html, number, title)
#     else:
#         return True


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


# timestmap = time.strptime(timeout + ":00", "%Y/%m/%d %H:%M:%S")
#     timeout = time.strftime("%Y-%m-%d %H:%M:%S", timestmap)