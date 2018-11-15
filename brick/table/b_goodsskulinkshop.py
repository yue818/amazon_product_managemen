# -*- coding: utf-8 -*-
class b_goodsskulinkshop():
    def __init__(self,db_conn=None,redis_conn=None):
        self.db_conn = db_conn
        self.redis_conn = redis_conn
        self.table_name ='py_db.b_goodsskulinkshop'

    def get_sku_by_shopsku(self,shopsku):
        sku = None
        if self.redis_conn is not None:
            sku = self.redis_conn.get(shopsku)
            if sku is not None:
                print 'get sku from redis'
                return sku
        if self.db_conn is not None:
            cursor =self.db_conn.cursor()
            sql = 'select sku from %s where shopsku = \'%s\' ' %(self.table_name,shopsku)
            print 'sql =%s' % sql
            #cursor.execute(sql,(self.table_name,shopsku,))
            cursor.execute(sql)
            b_goodsskulinkshop_obj = cursor.fetchone()
            if b_goodsskulinkshop_obj is None  or len(b_goodsskulinkshop_obj) <=0 or b_goodsskulinkshop_obj[0] is None:
                cursor.close()
                print 'no data in db'
                return None

            sku = b_goodsskulinkshop_obj[0]
            if self.redis_conn is not None:
                self.redis_conn.set(shopsku,sku)
                print 'set sku from db to redis'
            cursor.close()
            return sku
        return sku

