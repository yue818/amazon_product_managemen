#-*-coding:utf-8-*-

"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_wish_product_sku_upload_or_not_log.py
 @time: 2018-01-25 19:08
"""
class t_wish_product_sku_upload_or_not_log():
    def __init__(self,dbconn):
        self.dbconn = dbconn

    def insert_data(self,param):
        inscur = self.dbconn.cursor()
        inscur.execute("insert into t_wish_product_sku_upload_or_not_log "
                       "(sku,shopsku,`type`,person,`time`,status) "
                       "VALUES (%s,%s,%s,%s,%s,%s) ;",
                       (param['SKU'],param['ShopSKU'],param['Type'],
                        param['Person'],param['Time'],param['Status']))
        inscur.execute("commit;")
        inscur.close()