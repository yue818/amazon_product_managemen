#-*-coding:utf-8-*-
import datetime

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_download_info.py
 @time: 2018/1/4 15:01
"""

class t_download_info():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def insert_into_download_info(self, params):
        shocur = self.db_conn.cursor()
        shocur.execute("insert into t_download_info (appname,abbreviation,Datasource,Belonger,updatetime) values(%s,%s,%s,%s,%s);",
                       (params['appname'], params['abbreviation'],params['Datasource'], params['Belonger'],datetime.datetime.now()))
        shocur.execute("commit;")
        shocur.close()
