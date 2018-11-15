# coding: utf-8
"""
@author: wangzy
@contact: 15205512335
@site:
@software: PyCharm
@file: py_redis_log.py
@time: 2018-01-28 15:21
"""
import copy
import datetime, time, calendar
from py_SynRedis_pub import py_SynRedis_pub

class py_redis_log:
    synPub = py_SynRedis_pub()

    def get_time_stamp(self):
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - long(ct)) * 1000000
        time_stamp = "%s.%06d" % (data_head, data_secs)
        return time_stamp

    def getTimeDiff(self, timeStra, timeStrb):
        if timeStra <= timeStrb:
            return 0
        #print('{},{}'.format(timeStra,timeStrb))
        timeListStra = timeStra.split('.')
        timeListStrb = timeStrb.split('.')
        ta = time.strptime(timeListStra[0],"%Y-%m-%d %H:%M:%S")
        tb = time.strptime(timeListStrb[0],"%Y-%m-%d %H:%M:%S")
        y, m, d, H, M, S = ta[0:6]
        dataTimea = datetime.datetime(y, m, d, H, M, S)
        y, m, d, H, M, S = tb[0:6]
        dataTimeb = datetime.datetime(y, m, d, H, M, S)
        secondsDiff = (dataTimea - dataTimeb).seconds
        millDiff = int(timeListStra[1]) - int(timeListStrb[1])
        if millDiff < 0:
            millDiff = millDiff + 1000000
            secondsDiff -= 1
        strMillDiff = float(millDiff)/1000000.0
        #minutesDiff = round(secondsDiff / 60, 1)
        return secondsDiff + strMillDiff

    '''
    说明：日志记录写入redis
    '''
    def write_redis_log(self,logTable,strTime = '',nRecord = 0):
        sList = self.synPub.sList = self.synPub.getFromHashRedis(logTable,'',strTime)
        sArrayList = []

        if cmp(str(sList), 'None') == 0 or sList == -1 or strTime == '':
            strTime = self.get_time_stamp()
            sTmpArray = []
            sTmpArray.append(nRecord)
            sTmpArray.append(strTime)
            self.synPub.setToValuesHashRedis(logTable,strTime,sTmpArray)
        else:
            preDealCount = sList[0]
            preDealTime = sList[1]
            currentDate = self.get_time_stamp()
            strProcTime = self.getTimeDiff(currentDate,preDealTime)

            #print('{},{},{},{}'.format(preDealCount,preDealTime,currentDate,strProcTime))
            sTmpArray = []
            sTmpArray.append(int(preDealCount) + nRecord)
            sTmpArray.append(strProcTime)
            self.synPub.setToValuesHashRedis(logTable, strTime, sTmpArray)
        return strTime

'''
tLog = py_redis_log()
tLog.write_redis_log('t_goodsku','2018-02-08 16:29:56.015181',50)
'''