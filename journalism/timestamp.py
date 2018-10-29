import time


def seconds(timeout, exist=False):
    if exist:
        dt = timeout + ":00"
        # 转换成时间数组
        timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
        # 转换成时间戳
        timestamp = time.mktime(timeArray)
        return int(timestamp * 1000)
    else:
        dt = timeout
        # 转换成时间数组
        timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
        # 转换成时间戳
        timestamp = time.mktime(timeArray)
        return int(timestamp * 1000)
