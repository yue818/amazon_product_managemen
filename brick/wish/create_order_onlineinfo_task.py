# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: create_order_onlineinfo_task.py
 @time: 2018-01-09 19:42

"""   
# -*- coding: utf-8 -*-
#import logging
from datetime import datetime
class create_order_onlineinfo_task():
    def __init__(self,db_conn):
        self.db_conn = db_conn
        self.cmdid = ['GetListOrders','GetShopSKUInfo']
        self.PlatformName = 'Wish'

    def Get_order_online_info_data(self):
        cursor =self.db_conn.cursor()
        cursor.execute(u"select TRIM(name) from t_config_online_amazon where K= 'access_token' AND TRIM(name) in (SELECT DISTINCT ShopName_temp from t_store_configuration_file where Status='0');")
        objs= cursor.fetchall()
        cursor.close()
        OneCmdRecoreDict_dict = []
        for obj in objs:
            OneCmdRecoreDict ={}
            if obj:
                OneCmdRecoreDict['ShopName']          = obj[0]
                OneCmdRecoreDict['PlatformName']      = self.PlatformName
                OneCmdRecoreDict['CMDID']             = self.cmdid
                OneCmdRecoreDict['ScheduleTime']      = ''
                OneCmdRecoreDict['ActualBeginTime']   = datetime.now()
                OneCmdRecoreDict['ActualEndTime']     = ''
                OneCmdRecoreDict['Status']            = 0
                OneCmdRecoreDict['ProcessingStatus']  = ''
                OneCmdRecoreDict['Processed']         = 0
                OneCmdRecoreDict['Successful']        = 0
                OneCmdRecoreDict['WithError']         = 0
                OneCmdRecoreDict['WithWarning']       = ''
                OneCmdRecoreDict['TransactionID']     = ''
                OneCmdRecoreDict['InsertTime']        = datetime.now()
                OneCmdRecoreDict['UpdateTime']        = datetime.now()
                OneCmdRecoreDict['Params']            = ''
                OneCmdRecoreDict['Timedelta']         = 0
                OneCmdRecoreDict['RetryCount']        = 0
                OneCmdRecoreDict['pid']               = ''
                OneCmdRecoreDict['cmdtext']           = ''
                OneCmdRecoreDict['errorinfo']         = ''

                OneCmdRecoreDict_dict.append(OneCmdRecoreDict)
        return OneCmdRecoreDict_dict