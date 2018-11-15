# coding: utf-8
"""
@author: wangzy
@contact: 15205512335
@site:
@software: PyCharm
@file: py_Redis_diff.py
@time: 2018-02-06 15:21
"""
import sys
import os
import datetime, time, calendar
from py_SynRedis_tables import py_SynRedis_tables


if __name__ == "__main__":
    #print('{},{}'.format(sys.argv[0],sys.argv[1]))
    try:
        nextIndex = 1
        if len(sys.argv[1]) == 0:
            print('no agrv[1]')
        nextIndex = int(sys.argv[1])
        cmpPyData = py_SynRedis_tables()
        startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print('startTime={}'.format(startTime))
        while 1:
            print(nextIndex)
            strSKUID,gDicSKU,nextIndex = cmpPyData.ReadSKUFromFile(nextIndex)
            #print('sArraySKUID={},gDicSKU={},nextIndex={}'.format(strSKUID,gDicSKU,nextIndex))
            if len(strSKUID) == 0:
                continue
            sResult = cmpPyData.CheckPyAndRedisDiff(strSKUID,gDicSKU)
            if len(sResult) != 0:
                cmpPyData.WriteDiffResultToFile(sResult)
            if nextIndex == -1 or nextIndex == 0:
                break
        endTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print('startTime={}'.format(endTime))
    except IOError:
        print('open file fail:{}'.format(sys.argv[1]))
        cmpPyData.closeSql()