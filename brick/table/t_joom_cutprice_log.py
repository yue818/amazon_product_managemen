# -*- coding: utf-8 -*-

from brick.db.dbconnect import execute_db
from joom_app.table.t_joom_cutprice_log import t_joom_cutprice_log as t_joom_cutprice_log_table


class t_joom_cutprice_log():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def getlogbyproductid(self, product_id):
        product_sql = "SELECT ShopSKU, OldPrice, Discount, ShopName FROM t_joom_cutprice_log WHERE ProductID='%s'" % product_id
        product_res = execute_db(product_sql, self.db_conn, 'select')
        if not product_res:
            res = t_joom_cutprice_log_table.objects.filter(ProductID=product_id).values('ShopSKU', 'OldPrice', 'Discount')
            product_res = res
        return product_res

    def get_cutpricing_products(self):
        cutprice_products_sql = "SELECT * FROM t_joom_cutprice_log WHERE RecoverResult IS NULL OR RecoverResult='SOME SUCCESS' OR RecoverResult='ALL FALIED';"
        products = execute_db(cutprice_products_sql, self.db_conn, 'select')
        return products
