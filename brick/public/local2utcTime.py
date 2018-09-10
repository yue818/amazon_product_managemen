#-*-coding:utf-8-*-
import datetime,time
"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: local2utcTime.py
 @time: 2017/12/27 8:34
"""
def local2utc(local_time):
    """本地时间转UTC时间（-8:00）"""
    time_struct = time.mktime(local_time.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st

