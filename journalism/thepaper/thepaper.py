import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def storage(number, title, author, timeout, create_time, format_text, source):
    dicts = {
        "source_id": number,
        "source_url": "cn.youth.news",
        "newsType": "news",
        "title": title,
        "author": author,
        "release_time": timeout,
        "create_time": create_time,
        "format_text": format_text,
        "source": source,
    }
    print(dicts)
    # storageDatabase(dicts)



def download(html, number):
    pattern = re.compile('<video')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('<div class="newscontent"[\s\S]*?<div id="one"')
    data = re.findall(pattern, html)
    if data:
        data = data[0]
    else:
        return
    pattern_source = re.compile('来源：澎湃新闻')
    source = re.findall(pattern_source, data)
    if not source:
        return
    pattern_title = re.compile('(<h1 class="news_title">)([\s\S]*?)(</h1>)')
    title = re.findall(pattern_title, data)[0][1]
    pattern_time = re.compile('\d+-\d+-\d+ \d+:\d+')
    timeout = re.findall(pattern_time, data)[0]
    create_time = seconds(timeout, exist=True)
    pattern_author = re.compile('(>责任编辑：)([\s\S]*?)(<)')
    author = re.findall(pattern_author, data)[0][1]
    pattern_text = re.compile('(<div class="news_txt"[\s\S]*?>)([\s\S]*?)(<audio)')
    format_text = re.findall(pattern_text, data)
    if format_text:
        format_text = format_text[0][1]
    else:
        pattern_text = re.compile('(<div class="news_txt"[\s\S]*?>)([\s\S]*?)(</div>[\s\S]*?<div class="go_to_topic">)')
        format_text = re.findall(pattern_text, data)[0][1]
    pattern = re.compile('<div[\s\S]*?>')
    format_text = re.sub(pattern, "<p>", format_text)
    pattern = re.compile('</div>')
    format_text = re.sub(pattern, "</p>", format_text)
    storage(number, title, author, timeout, create_time, format_text, source)


def createLinks(url, number):
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = reponse.text
        download(html, number)
    else:
        return "end"


def getURL(html, n, i):
    data = []
    if n == 1:
        if i == "https://www.thepaper.cn/channel_36079":
            pattern = re.compile('<div class="paike_newsbox" id="masonryContent"[\s\S]*?<script type="text/javascript">')
            html = re.findall(pattern, html)[0]
        elif i == "https://www.thepaper.cn/gov_publish.jsp":
            pattern = re.compile('<div class="publish_top">[\s\S]*?<div class="recommend_politics">')
            msg = re.findall(pattern, html)[0]
            pattern = re.compile('<h2>[\s\S]*?</h2>')
            data = re.findall(pattern, msg)
            pattern = re.compile('<div id="mainContent">[\s\S]*?<script type="text/javascript">')
            html = re.findall(pattern, html)[0]
        else:
            pattern = re.compile('<div class="pdtt_rtbd">[\s\S]*?</div>')
            msg = re.findall(pattern, html)[0]
            data.append(msg)
            pattern = re.compile('<div id="mainContentChan">[\s\S]*?<script type="text/javascript">')
            html = re.findall(pattern, html)[0]
    pattern = re.compile('<h2>[\s\S]*?</h2>')
    urls = re.findall(pattern, html)
    data = data + urls
    for message in data:
        pattern = re.compile('(href=")([\s\S]*?)(")')
        incomplete_url = re.findall(pattern, message)[0][1]
        pattern = re.compile("\d+")
        number = int(re.findall(pattern, incomplete_url)[0])
        # if rechecking(number, source_url="cn.thepaper.www"):
        #     return "end"
        url = "https://www.thepaper.cn/" + incomplete_url
        badmsg = createLinks(url, number)
        if badmsg == "end":
            return "end"
    pattern = re.compile('(lastTime=")([\s\S]*?)(")')
    lastTime = re.findall(pattern, html)
    if lastTime:
        return lastTime[0][1]


def combination(i, n, lastTime):
    if n == 1:
        url = i
    else:
        if i == "https://www.thepaper.cn/channel_25950":
            url = "https://www.thepaper.cn/load_index.jsp?nodeids=25462,25488,25489,25490,25423,25426,25424,\
25463,25491,25428,27604,25464,25425,25429,25481,25430,25678,25427,25422,25487,25634,25635,25600,\
&topCids=2483860,2484422,2485650&pageidx=%s&lastTime=%s" % (n, lastTime)
        elif i == "https://www.thepaper.cn/channel_25951":
            url = "https://www.thepaper.cn/load_index.jsp?nodeids=25434,25436,25433,25438,25435,25437,27234,25485,\
25432,37978,&topCids=2486856,2486883,2486846&pageidx=%s&lastTime=%s" % (n, lastTime)
        elif i == "https://www.thepaper.cn/channel_25952":
            url = "https://www.thepaper.cn/load_index.jsp?nodeids=25444,27224,26525,26878,25483,25457,25574,25455,\
26937,25450,25482,25445,25456,25446,25536,26506,&topCids=2481336&pageidx=%s&lastTime=%s" % (n, lastTime)
        elif i == "https://www.thepaper.cn/channel_25953":
            url = "https://www.thepaper.cn/load_index.jsp?nodeids=25448,26609,25942,26015,25599,25842,26862,25769,\
25990,26173,26202,26404,26490,&topCids=2486782,2482397,2484232&pageidx=%s&lastTime=%s" % (n, lastTime)
        elif i == "https://www.thepaper.cn/channel_36079":
            url = "https://www.thepaper.cn/load_sparker_masnory.jsp?nodeids=35571,35570,35572,&topCids=2483223,\
2482384,2482801,2483340,2486815,&pageidx=%s&isList=false&isUser=&userIds=&lastTime=%s" % (n, lastTime)
        elif i == "https://www.thepaper.cn/gov_publish.jsp":
            url = "https://www.thepaper.cn/load_more_gov.jsp?nodeids=&topCids=2486451,2486564,2486598,2487128,\
2487213,2485569,2487248,2486308,2486148,2486292,2485748,2486144,2486715,2486235,2485593,2486680\
&pageidx=%s&govType=publish" % n
        else:
            url = "https://www.thepaper.cn"
    return url


def starts():
    urls = ["https://www.thepaper.cn/channel_25950", "https://www.thepaper.cn/channel_25951",
            "https://www.thepaper.cn/channel_36079", "https://www.thepaper.cn/channel_25952",
            "https://www.thepaper.cn/channel_25953", "https://www.thepaper.cn/gov_publish.jsp"]
    for i in urls:
        n = 1
        lastTime = ""
        while True:
            url = combination(i, n, lastTime)
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            if reponse.status_code == 200:
                html = reponse.text
                data = getURL(html, n, i)
                if data == "end":
                    break
                lastTime = data
                n += 1
            else:
                break


if __name__ == '__main__':
    starts()