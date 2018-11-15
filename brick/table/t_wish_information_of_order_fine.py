#-*-coding:utf-8-*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_wish_information_of_order_fine.py
 @time: 2018/8/9 10:03
"""
class t_wish_information_of_order_fine():
    def __init__(self, conn):
        self.conn = conn

    def insert(self, param):
        try:
            cursor = self.conn.cursor()

            sql = "insert into t_wish_information_of_order_fine set fine_id=%s, amount=%s, payment_deduction_amount=%s, " \
                  "timestamp_api=%s, status=%s, status_text=%s, fine_type=%s, fine_type_text=%s, is_reversed=%s, cancelled_time=%s, " \
                  "cancelled_reason_text=%s, order_id=%s,updatetime=now() " \
                  "on duplicate KEY update amount=%s, payment_deduction_amount=%s,timestamp_api=%s, status=%s, " \
                  "status_text=%s, fine_type=%s, fine_type_text=%s, is_reversed=%s, cancelled_time=%s," \
                  "cancelled_reason_text=%s, order_id=%s,updatetime=now();"

            parameter = [
                param.get('id'),param.get('amount'),param.get('payment_deduction_amount'),param.get('timestamp'),
                param.get('status'),param.get('status_text'),param.get('fine_type'),param.get('fine_type_text'),
                param.get('is_reversed'),param.get('cancelled_time'),param.get('cancelled_reason_text'),
                param.get('order_id'),
                # -----------------<分割线>-----------------
                param.get('amount'), param.get('payment_deduction_amount'), param.get('timestamp'),
                param.get('status'), param.get('status_text'), param.get('fine_type'), param.get('fine_type_text'),
                param.get('is_reversed'), param.get('cancelled_time'), param.get('cancelled_reason_text'),
                param.get('order_id'),
            ]

            cursor.execute(sql, parameter)
            cursor.execute("commit;")
            cursor.close()
            return {'errorcode': 1, 'errortext': '', 'param': param}
        except Exception as e:
            return {'errorcode': -1, 'errortext': u'{}'.format(e)}




