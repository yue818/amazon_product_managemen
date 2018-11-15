# coding=utf-8


from datetime import datetime


def get_time_stamp():
    """
    获取格式化的时间戳，可用于在控制台打印输出的信息
    返回值：时间戳 比如：[2017-12-27 13:48:53]
    """
    timeStamp = str(datetime.now())[:19]
    timeStamp = '[' + timeStamp + ']' + ' '
    return timeStamp