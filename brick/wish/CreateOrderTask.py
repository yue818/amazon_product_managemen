# -*- coding: utf-8 -*-
#import logging
import datetime
class CreateOrderTask():
    def __init__(self,db_conn):
        self.db_conn = db_conn
        self.cmdid ='GetListOrders'
        self.PlatformName = 'Wish'

    def CreateTasks(self):
        cursor =self.db_conn.cursor();
        sql= "insert into t_api_schedule_ing(ShopName,PlatformName,CMDID,Status,ScheduleTime,inserttime,updatetime,timedelta,retrycount) select  name, \'Wish\',\'GetListOrders\',0, now(),now(),now(),1200,0 from t_config_online_amazon where K= \'access_token\' ";
        cursor.execute(sql)
        cursor.close()
        self.db_conn.commit()


    def GetTasks(self):
        self.PlatformName = 'Wish'
        cursor =self.db_conn.cursor()
        sql = u"select id,ShopName,PlatformName,CMDID,ScheduleTime,ActualBeginTime,ActualEndTime,Status,ProcessingStatus,Processed,Successful,WithError,WithWarning,TransactionID,InsertTime,UpdateTime,Params,Timedelta,RetryCount from t_api_schedule_ing  where  PlatformName=\'%s\' and cmdid =\'%s\' and  ScheduleTime <= NOW() order by ScheduleTime  "%(
                                                                self.PlatformName,self.cmdid)
        print 'getAllCmdWish sql=%s'%sql
        #logging.debug( 'GetTasks sql=%s'%sql)
        n= cursor.execute(sql)
        print 'getAllh n=%s' % n
        t_api_schedule_ing_objs= cursor.fetchall()
        OneCmdRecoreDict_list=[]
        print 'getAllCmdWish ..........n=%s' % n
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
                OneCmdRecoreDict['pid']               = ''
                OneCmdRecoreDict['cmdtext']           = ''
                OneCmdRecoreDict['errorinfo']         = ''
                OneCmdRecoreDict_list.append(OneCmdRecoreDict)
                print t_api_schedule_ing_obj
        cursor.close()

        return OneCmdRecoreDict_list
    def GetTasksV2(self):

        cursor =self.db_conn.cursor()
        sql = u"select TRIM(name) from t_config_online_amazon where K= \'access_token\'"

        print 'getAllCmdWish sql=%s'%sql
        #logging.debug( 'GetTasks sql=%s'%sql)
        n= cursor.execute(sql)
        print 'getAllh n=%s' % n
        t_api_schedule_ing_objs= cursor.fetchall()
        OneCmdRecoreDict_dict = {}
        print 'getAllCmdWish ..........n=%s' % n
        for t_api_schedule_ing_obj in t_api_schedule_ing_objs:
            OneCmdRecoreDict ={}
            if t_api_schedule_ing_obj is not None:

                OneCmdRecoreDict['ShopName']          = t_api_schedule_ing_obj[0]
                OneCmdRecoreDict['PlatformName']      = self.PlatformName
                OneCmdRecoreDict['CMDID']             = self.cmdid
                OneCmdRecoreDict['ScheduleTime']      = ''
                OneCmdRecoreDict['ActualBeginTime']   = datetime.datetime.now()
                OneCmdRecoreDict['ActualEndTime']     = ''
                OneCmdRecoreDict['Status']            = 0
                OneCmdRecoreDict['ProcessingStatus']  = ''
                OneCmdRecoreDict['Processed']         = 0
                OneCmdRecoreDict['Successful']        = 0
                OneCmdRecoreDict['WithError']         = 0
                OneCmdRecoreDict['WithWarning']       = ''
                OneCmdRecoreDict['TransactionID']     = ''
                OneCmdRecoreDict['InsertTime']        = datetime.datetime.now()
                OneCmdRecoreDict['UpdateTime']        = datetime.datetime.now()
                OneCmdRecoreDict['Params']            = ''
                OneCmdRecoreDict['Timedelta']         = 0
                OneCmdRecoreDict['RetryCount']        = 0
                OneCmdRecoreDict['pid']               = ''
                OneCmdRecoreDict['cmdtext']           = ''
                OneCmdRecoreDict['errorinfo']         = ''

                OneCmdRecoreDict_dict[t_api_schedule_ing_obj[0]] = OneCmdRecoreDict
                print t_api_schedule_ing_obj
        cursor.close()

        return OneCmdRecoreDict_dict