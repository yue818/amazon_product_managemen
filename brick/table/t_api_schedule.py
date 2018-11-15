# -*- coding: utf-8 -*-
import logging
import os, datetime
from brick.wish.wish_api_before.token_verification import verb_token

class t_api_schedule():
    def __init__(self,auth_info,cnxn,redis_conn):
        self.PlatformName = None
        self.ShopName = None
        self.auth_info = auth_info
        if auth_info and auth_info.has_key('PlatformName'):
            self.PlatformName = auth_info['PlatformName']
        if auth_info and auth_info.has_key('ShopName'):
            self.ShopName = auth_info['ShopName']

        self.cnxn = cnxn
        self.redis_conn = redis_conn

    def getauthByShopName(self,ShopName):
        ainfo = verb_token(ShopName, self.cnxn)
        assert ainfo['errorcode'] == 1, ainfo['errortext']

        self.auth_info = ainfo['auth_info']
        return ainfo['auth_info']

    def getOneCmd(self):
        cursor =self.cnxn.cursor()
        sql = u"select id,ShopName,PlatformName,CMDID,ScheduleTime,ActualBeginTime,ActualEndTime,Status,ProcessingStatus,Processed,Successful,WithError,WithWarning,TransactionID,InsertTime,UpdateTime,Params,Timedelta,RetryCount from t_api_schedule_ing  where  ShopName=%s and PlatformName=%s and  ScheduleTime <= NOW() and RetryCount < 5 order by ScheduleTime LIMIT 0,1 "

        print 'getOneCmd sql=%s'%sql
        cursor.execute(sql,(self.ShopName,self.PlatformName))
        t_api_schedule_ing_obj= cursor.fetchone()

        OneCmdRecoreDict ={}
        if t_api_schedule_ing_obj is not None:
            OneCmdRecoreDict['id']                = t_api_schedule_ing_obj[0]
            OneCmdRecoreDict['ShopName']          = t_api_schedule_ing_obj[1]
            OneCmdRecoreDict['PlatformName']      = t_api_schedule_ing_obj[2]
            OneCmdRecoreDict['CMDID']             = t_api_schedule_ing_obj[3]
            OneCmdRecoreDict['ScheduleTime']      = t_api_schedule_ing_obj[4]
            OneCmdRecoreDict['ActualBeginTime']   = t_api_schedule_ing_obj[5]
            OneCmdRecoreDict['ActualEndTime']     = t_api_schedule_ing_obj[6]
            OneCmdRecoreDict['Status']            = t_api_schedule_ing_obj[7]
            OneCmdRecoreDict['ProcessingStatus']  = t_api_schedule_ing_obj[8]
            OneCmdRecoreDict['Processed']         = t_api_schedule_ing_obj[9]
            OneCmdRecoreDict['Successful']        = t_api_schedule_ing_obj[10]
            OneCmdRecoreDict['WithError']         = t_api_schedule_ing_obj[11]
            OneCmdRecoreDict['WithWarning']       = t_api_schedule_ing_obj[12]
            OneCmdRecoreDict['TransactionID']     = t_api_schedule_ing_obj[13]
            OneCmdRecoreDict['InsertTime']        = t_api_schedule_ing_obj[14]
            OneCmdRecoreDict['UpdateTime']        = t_api_schedule_ing_obj[15]
            OneCmdRecoreDict['Params']            = t_api_schedule_ing_obj[16]
            OneCmdRecoreDict['Timedelta']         = t_api_schedule_ing_obj[17]
            OneCmdRecoreDict['RetryCount']        = t_api_schedule_ing_obj[18]

            print t_api_schedule_ing_obj
        cursor.close()

        return OneCmdRecoreDict

    def getOneCmdWish(self):
        self.PlatformName = 'Wish'
        cursor =self.cnxn.cursor()
        sql = u"select id,ShopName,PlatformName,CMDID,ScheduleTime,ActualBeginTime,ActualEndTime,Status,ProcessingStatus,Processed,Successful,WithError,WithWarning,TransactionID,InsertTime,UpdateTime,Params,Timedelta,RetryCount,pid,cmdtext,errorinfo from t_api_schedule_ing  where (Status=\'0\' or pid=\'%s\')  and PlatformName=\'%s\' and  ScheduleTime <= NOW() and ( CMDID =\'%s\' or CMDID =\'%s\'  )  order by ScheduleTime LIMIT 0,1 "%(
                                                                os.getpid(),self.PlatformName,'GetShopSKUInfo','GetListOrders')
        print 'getOneCmd sql=%s'%sql
        cursor.execute(sql)
        t_api_schedule_ing_obj= cursor.fetchone()

        OneCmdRecoreDict ={}
        if t_api_schedule_ing_obj is not None:
            OneCmdRecoreDict['id']                = t_api_schedule_ing_obj[0]
            OneCmdRecoreDict['ShopName']          = t_api_schedule_ing_obj[1]
            OneCmdRecoreDict['PlatformName']      = t_api_schedule_ing_obj[2]
            OneCmdRecoreDict['CMDID']             = t_api_schedule_ing_obj[3]
            OneCmdRecoreDict['ScheduleTime']      = t_api_schedule_ing_obj[4]
            OneCmdRecoreDict['ActualBeginTime']   = t_api_schedule_ing_obj[5]
            OneCmdRecoreDict['ActualEndTime']     = t_api_schedule_ing_obj[6]
            OneCmdRecoreDict['Status']            = t_api_schedule_ing_obj[7]
            OneCmdRecoreDict['ProcessingStatus']  = t_api_schedule_ing_obj[8]
            OneCmdRecoreDict['Processed']         = t_api_schedule_ing_obj[9]
            OneCmdRecoreDict['Successful']        = t_api_schedule_ing_obj[10]
            OneCmdRecoreDict['WithError']         = t_api_schedule_ing_obj[11]
            OneCmdRecoreDict['WithWarning']       = t_api_schedule_ing_obj[12]
            OneCmdRecoreDict['TransactionID']     = t_api_schedule_ing_obj[13]
            OneCmdRecoreDict['InsertTime']        = t_api_schedule_ing_obj[14]
            OneCmdRecoreDict['UpdateTime']        = t_api_schedule_ing_obj[15]
            OneCmdRecoreDict['Params']            = t_api_schedule_ing_obj[16]
            OneCmdRecoreDict['Timedelta']         = t_api_schedule_ing_obj[17]
            OneCmdRecoreDict['RetryCount']        = t_api_schedule_ing_obj[18]
            OneCmdRecoreDict['pid']               = os.getpid()
            OneCmdRecoreDict['cmdtext']           = t_api_schedule_ing_obj[20]
            OneCmdRecoreDict['errorinfo']         = t_api_schedule_ing_obj[21]
            print t_api_schedule_ing_obj

            sql_update = u"update t_api_schedule_ing set Status =\'1\',pid=%s where id = %s "

            print sql_update
            cursor.execute(sql_update,(os.getpid(),t_api_schedule_ing_obj[0]))
            self.cnxn.commit()

        cursor.close()

        return OneCmdRecoreDict



    def getAllCmdWish(self):
        self.PlatformName = 'Wish'
        cursor =self.cnxn.cursor()
        sql = u"select id,ShopName,PlatformName,CMDID,ScheduleTime,ActualBeginTime,ActualEndTime,Status,ProcessingStatus,Processed,Successful,WithError,WithWarning,TransactionID,InsertTime,UpdateTime,Params,Timedelta,RetryCount from t_api_schedule_ing  where  PlatformName=\'%s\' and  ScheduleTime <= NOW() order by ScheduleTime  "%(
                                                                self.PlatformName)
        print 'getAllCmdWish sql=%s'%sql
        cursor.execute(sql)
        t_api_schedule_ing_objs= cursor.fetchall()
        OneCmdRecoreDict_list=[]
        for t_api_schedule_ing_obj in t_api_schedule_ing_objs:
            OneCmdRecoreDict ={}
            if t_api_schedule_ing_obj is not None:
                OneCmdRecoreDict['id']                = t_api_schedule_ing_obj[0]
                OneCmdRecoreDict['ShopName']          = t_api_schedule_ing_obj[1]
                OneCmdRecoreDict['PlatformName']      = t_api_schedule_ing_obj[2]
                OneCmdRecoreDict['CMDID']             = t_api_schedule_ing_obj[3]
                OneCmdRecoreDict['ScheduleTime']      = t_api_schedule_ing_obj[4]
                OneCmdRecoreDict['ActualBeginTime']   = t_api_schedule_ing_obj[5]
                OneCmdRecoreDict['ActualEndTime']     = t_api_schedule_ing_obj[6]
                OneCmdRecoreDict['Status']            = t_api_schedule_ing_obj[7]
                OneCmdRecoreDict['ProcessingStatus']  = t_api_schedule_ing_obj[8]
                OneCmdRecoreDict['Processed']         = t_api_schedule_ing_obj[9]
                OneCmdRecoreDict['Successful']        = t_api_schedule_ing_obj[10]
                OneCmdRecoreDict['WithError']         = t_api_schedule_ing_obj[11]
                OneCmdRecoreDict['WithWarning']       = t_api_schedule_ing_obj[12]
                OneCmdRecoreDict['TransactionID']     = t_api_schedule_ing_obj[13]
                OneCmdRecoreDict['InsertTime']        = t_api_schedule_ing_obj[14]
                OneCmdRecoreDict['UpdateTime']        = t_api_schedule_ing_obj[15]
                OneCmdRecoreDict['Params']            = t_api_schedule_ing_obj[16]
                OneCmdRecoreDict['Timedelta']         = t_api_schedule_ing_obj[17]
                OneCmdRecoreDict['RetryCount']        = t_api_schedule_ing_obj[18]
                OneCmdRecoreDict_list.append(OneCmdRecoreDict)
                print t_api_schedule_ing_obj
        cursor.close()

        return OneCmdRecoreDict_list

    def updateOneCmd(self,OneCmdRecoreDict):
        cursor =self.cnxn.cursor()
        sql = u"update t_api_schedule_ing set ActualBeginTime=%s, TransactionID = %s ,ScheduleTime = %s,Status =%s ,ProcessingStatus = %s, ActualEndTime =  %s , Timedelta =  %s, RetryCount =  %s,pid=%s ,cmdtext = %s ,errorinfo = %s where  id=%s  "

        print 'updateOneCmd sql=%s'%sql
        cursor.execute(sql,(OneCmdRecoreDict['ActualBeginTime'] ,OneCmdRecoreDict['TransactionID'],OneCmdRecoreDict['ScheduleTime'],OneCmdRecoreDict['Status'],OneCmdRecoreDict['ProcessingStatus'],OneCmdRecoreDict['ActualEndTime'],OneCmdRecoreDict['Timedelta'],OneCmdRecoreDict['RetryCount'],OneCmdRecoreDict['pid'],OneCmdRecoreDict['cmdtext'],OneCmdRecoreDict['errorinfo'],OneCmdRecoreDict['id']))
        self.cnxn.commit()

    def moveOneCmd(self,OneCmdRecoreDict):
        self.insertOneCmd(OneCmdRecoreDict)
        #self.deleteOneCmd(OneCmdRecoreDict)
        self.cnxn.commit()
    def insertOneCmd(self,OneCmdRecoreDict):
        cursor =self.cnxn.cursor()
        sql = "insert into t_api_schedule_ed (ShopName,PlatformName,CMDID,ScheduleTime,ActualBeginTime,ActualEndTime,Status,ProcessingStatus,Processed,Successful,WithError,WithWarning,TransactionID,InsertTime,Params,Timedelta,RetryCount,pid,cmdtext,errorinfo) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); "
        #%(

        print 'insertOneCmd sql=%s'%sql
        cursor.execute(sql,(OneCmdRecoreDict['ShopName'],OneCmdRecoreDict['PlatformName'],OneCmdRecoreDict['CMDID'],OneCmdRecoreDict['ScheduleTime'],
                           OneCmdRecoreDict['ActualBeginTime'],OneCmdRecoreDict['ActualEndTime'],OneCmdRecoreDict['Status'],OneCmdRecoreDict['ProcessingStatus'],OneCmdRecoreDict['Processed'],
                           OneCmdRecoreDict['Successful'],OneCmdRecoreDict['WithError'],OneCmdRecoreDict['WithWarning'],OneCmdRecoreDict['TransactionID'],OneCmdRecoreDict['InsertTime'],
                           OneCmdRecoreDict['Params'],OneCmdRecoreDict['Timedelta'],OneCmdRecoreDict['RetryCount'],OneCmdRecoreDict['pid'],OneCmdRecoreDict['cmdtext'] ,OneCmdRecoreDict['errorinfo']))
    def deleteOneCmd(self,OneCmdRecoreDict):
        cursor =self.cnxn.cursor()
        sql = u"delete from t_api_schedule_ing  where  id=\'%s\'"%(OneCmdRecoreDict['id'])
        print 'deleteOneCmd sql=%s'%sql
        cursor.execute(sql)

    #2倍指数增加
    def refreshScheduleTimeAndTimedelta(self,OneCmdRecoreDict):
        OneCmdRecoreDict['ScheduleTime'] = datetime.datetime.now() + datetime.timedelta(seconds = OneCmdRecoreDict['Timedelta'])
        OneCmdRecoreDict['Timedelta'] = OneCmdRecoreDict['Timedelta'] *2
        OneCmdRecoreDict['RetryCount'] += 1