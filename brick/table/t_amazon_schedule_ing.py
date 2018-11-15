#-*-coding:utf-8-*-


"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_amazon_schedule_ing.py
 @time: 2018/2/6 14:39
"""   
class t_amazon_schedule_ing():
    def __init__(self,db_conn=None):
        self.cnxn = db_conn

    def insert_need_feed_amazon_info(self,params):
        cursor = self.cnxn.cursor()
        sql = "insert into t_amazon_schedule_ing (ShopName,ShopNameIP,PlatformName,CMDID,ScheduleTime,Status,InsertTime,UpdateTime," \
              "Timedelta,RetryCount,Processed,Successful,WithError,WithWarning,Params) values ('%s','%s','Amazon','amazon_feed_track'," \
              "'%s','0','%s','%s',5,0,0,0,0,0,'%s')" % (params['shopName'],params['ShopNameIP'],params['insert_time'],params['insert_time'],
                                                  params['insert_time'],params['request_str'])
        cursor.execute(sql)
        cursor.close()