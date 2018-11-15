# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_shopsku_information_binding.py
 @time: 2017-12-15 12:40

"""

class t_shopsku_information_binding():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    # INSERT_INTO_SHOPSKU_INFORMATION_BINGDING
    def insert_into_shopsku_information_banding(self, params):
        result = {}
        try:
            bancur = self.db_conn.cursor()
            bancur.execute("insert into t_shopsku_information_binding " 
                           "(SKU,ShopSKU,Memo,PersonCode,Filename,SubmitTime,BindingStatus) "  
                           "values (%s,%s,%s,%s,%s,now(),'wait')", (params['SKU'], params['ShopSKU'], params['Memo'], params['Seller'], params['Theway']))
            bancur.execute('commit;')
            bancur.close()
            result['code'] = 0
            result['error'] = ''
        except Exception,ex:
            result['code'] = 1
            result['error'] = '%s:%s'%(Exception,ex)
        return result


    def The_earliest_binding_time(self,sku,seller):
        earsor = self.db_conn.cursor()
        earsor.execute("select MIN(ApplyTime) from py_db.t_log_sku_shopsku WHERE SKU=%s and `Status` = 'APPLYSUCCESS'  and StaffName=%s;",(sku,seller))
        obj = earsor.fetchone()
        earsor.close()
        return obj













