import re
import json
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def download(html, message):
    pattern = re.compile("")


def connect(message):
    url = message["titleurl"]
    pattern = re.compile('cqcb')
    exist = re.findall(pattern, url)
    if not exist:
        return
    print(url)
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    # if response.status_code == 200:
    #     html = response.text
    #     download(html, message)


def getURL(html):
    print(html)
    data = json.loads(html)
    print(data)
    news = data["newslist"]
    for message in news:
        number = int(message["id"])
        # if rechecking(number, source_url="com.cqcb.www"):
        #     return True
        mistake = connect(message)
        if mistake:
            return True


def starts():
    urls = ["http://www.cqcb.com/highlights/index.json", "http://www.cqcb.com/shishi/index.json",
            "http://www.cqcb.com/entertainment/index.json", "http://www.cqcb.com/science/index.json"]
    for i in urls:
        n = 1
        while True:
            if n == 1:
                url = i
            else:
                page = "_" + str(n) + ".json"
                url = re.sub(".json", page, i)
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