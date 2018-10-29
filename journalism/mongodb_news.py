import pymongo
import time
"""
数据存储在一张表中，使用三组数据进行确认；
数据在源网站的id值；
数据的源网站的网址；
数据的信息类型。
"""


# 连接数据库
conn = pymongo.MongoClient('localhost', 27017)
db = conn['journalism']


# 打开数据库的错误信息集合
def errorMessage(dicts):
    cursor = db['error']
    storage_time = time.asctime(time.localtime(time.time()))
    dicts["storage_time"] = storage_time
    cursor.insert_one(dicts)


# 打开对应数据库集合，存入数据
def storageDatabase(dicts):
    cursor = db['news']
    storage_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    dicts["storage_time"] = storage_time
    cursor.insert_one(dicts)


def rechecking(number, source_url, newsType="news"):
    # 查询对应数据库是否已经存在
    cursor = db['news']
    my_set = cursor.find({"source_id": number, "source_url":source_url, "newsType":newsType})
    num = my_set.count()
    if num == 1:
        return True
    elif num == 0:
        return False


def max_id(source_url, newsType="news"):
    # 查询编号最大值
    cursor = db['news']
    my_set = cursor.find({"source_url":source_url, "newsType":newsType}).sort([("source_id", -1)]).limit(1)
    num = my_set.count()
    if num == 1:
        return True
    elif num == 0:
        return False


def title_find(title, source_url, newsType="news"):
    # 使用标题进行查询是否存入过
    cursor = db["news"]
    my_set = cursor.find({"title": title, "source_url":source_url, "newsType":newsType})
    num = my_set.count()
    if num == 1:
        return True
    elif num == 0:
        return False


def closeMongodb():
    conn.close()

