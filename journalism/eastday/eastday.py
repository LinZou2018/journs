import re
import requests
import headers
from mongodb_news import rechecking, storageDatabase
from timestamp import seconds


def starts():
    urls = ["http://news.eastday.com/china/index.html",
            "http://news.eastday.com/world/index.html",
            "http://news.eastday.com/society/index.html",
            "http://mil.021east.com/",
            "http://finance.eastday.com/",
            "http://news.eastday.com/eastday/13news/auto/news/finance/index_K47.html",
            "http://news.eastday.com/eastday/13news/auto/news/sports/index_K48.html",
            "http://news.eastday.com/eastday/13news/auto/news/enjoy/index_K49.html"]


if __name__ == '__main__':
    starts()