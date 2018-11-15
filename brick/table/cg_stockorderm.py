#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: cg_stockorderm.py
 @time: 2018/1/17 16:30
"""

class cg_stockorderm():
    def __init__(self,db_conn):
        self.db_conn = db_conn

    def get_Logistics_number_Single_number(self,Single_number):
        logcur = self.db_conn.cursor()
        logcur.execute("select alibabaorderid,LogisticOrderNo from py_db.cg_stockorderm WHERE BillNumber = %s ;",(Single_number,))
        obj = logcur.fetchone()
        logcur.close()
        return obj
