#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_distribution_product_to_store_result.py
 @time: 2018-02-10 13:20
"""
class t_distribution_product_to_store_result():
    def __init__(self,db_conn):
        self.db_conn = db_conn

    def get_count_num(self,parentsku,shopname):
        parcur = self.db_conn.cursor()
        parcur.execute("select count(ParentSKU) from t_distribution_product_to_store_result WHERE "
                       "ParentSKU = %s AND ShopName = %s and Status = '1'; ",(parentsku,shopname))
        obj = parcur.fetchone()
        parcur.close()
        num = 0
        if obj:
            num = obj[0]
        return num