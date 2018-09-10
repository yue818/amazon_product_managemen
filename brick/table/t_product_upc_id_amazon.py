#-*-coding:utf-8-*-
from datetime import datetime

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: t_product_upc_id_amazon.py
 @time: 2018/3/26 20:28
"""   
class t_product_upc_id_amazon():
    def __init__(self, db_conn=None):
        self.cnxn = db_conn

    def get_newest_product_id(self, params):
        shocur = self.cnxn.cursor()
        shocur.execute(
            "select id,external_product_id from t_product_upc_id_amazon where id=%s;",
            (params['id'],))
        t_product_upc_id_amazon_obj = shocur.fetchone()
        t_product_upc_id_amazon = {}
        if t_product_upc_id_amazon_obj:
            t_product_upc_id_amazon['id'] = t_product_upc_id_amazon_obj[0]
            t_product_upc_id_amazon['external_product_id'] = t_product_upc_id_amazon_obj[1]
        shocur.close()
        return t_product_upc_id_amazon

    def delete_product_id(self, params):
        shocur = self.cnxn.cursor()
        shocur.execute("delete from t_product_upc_id_amazon where id = %s;",(params['id'],))
        self.cnxn.commit()
        shocur.close()

    def update_product_id(self, params):
        shocur = self.cnxn.cursor()
        shocur.execute('SET @update_id:= 0;')
        shocur.execute("UPDATE t_product_upc_id_amazon SET `use_status` = '3', id = (SELECT @update_id:= id), updateTime=%s, updateUser='online_auto'"
                       "WHERE  external_product_id_type = %s and use_status='1' LIMIT 1;", (datetime.now(), params['id_type']))
        shocur.execute('commit;')
        shocur.execute('SELECT @update_id;')
        t_product_upc_id_amazon_obj = shocur.fetchone()
        shocur.close()
        upc_id = 0
        if t_product_upc_id_amazon_obj:
            upc_id = t_product_upc_id_amazon_obj[0]
        return  upc_id

