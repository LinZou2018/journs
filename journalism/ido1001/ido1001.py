import re
import time
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def getURL(html):
    pattern = re.compile('<ul class="lis-ban-pic">[\s\S]*?</ul>')
    data = re.findall(pattern, html)
    pattern = re.compile('<section class="md md3">[\s\S]*?</section>')
    msg = data + re.findall(pattern, html)
    for dataOne in msg:
        pattern = re.compile('')


def starts():
    url = "https://idol001.com/"
    response = requests.get(url, headers=headers.header())
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        getURL(html)


if __name__ == '__main__':
    starts()