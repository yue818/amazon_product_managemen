#-*-coding:utf-8-*-
u"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_order_of_wish_fbw_fee.py
 @time: 2018/8/31 15:12
"""

class t_order_of_wish_fbw_fee():
    def __init__(self, connection):
        self.connection = connection

    def insert_fbw_fee(self, param):
        try:
            sql = "insert into t_order_of_wish_fbw_fee set currency=%s,amount=%s,fee_name=%s,fee_type_text=%s," \
                  "fee_type=%s,order_id=%s,fbw_warehouse_code=%s" \
                  " on duplicate KEY update  currency=%s,amount=%s,fee_name=%s,fee_type_text=%s,fee_type=%s," \
                  "fbw_warehouse_code=%s ; "

            cursor = self.connection.cursor()
            cursor.execute(sql,(param['currency'],param['amount'],param['fee_name'],param['fee_type_text'],
                           param['fee_type'],param['order_id'],param['fbw_warehouse_code'],
                           # ---------------------------------------------------------
                           param['currency'],param['amount'],param['fee_name'],param['fee_type_text'],param['fee_type'],
                           param['fbw_warehouse_code']))
            cursor.execute("commit;")
            cursor.close()
            return {'errorcode': 1, 'param': param}
        except Exception as error:
            return {'errorcode': -1, 'errortext': u'{}'.format(error), 'param': param}


