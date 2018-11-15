#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_chart_wish_refund_log.py
 @time: 2018-02-10 9:33
"""
class t_chart_wish_refund_log():
    def __init__(self,db_conn):
        self.db_conn = db_conn

    def insert_data_log(self,params):
        inscur = self.db_conn.cursor()
        inscur.execute("insert into t_chart_wish_refund_log (OrderID,OrderState,OrderFlag,"
                       "SaleDeleteFlag,RefundDeleteFlag) VALUES (%s,%s,%s,0,0)",
                       (params['OrderID'],params['OrderState'],params['OrderFlag']))
        inscur.execute('commit;')
        inscur.close()