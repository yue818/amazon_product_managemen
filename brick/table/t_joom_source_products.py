# -*- coding: utf-8 -*-

from brick.db.dbconnect import execute_db


class t_joom_source_products():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_all_source_products(self):
        sql = "SELECT id, ShopName, ProductsInfo FROM t_joom_source_products WHERE flag=0 LIMIT 1000;"
        res = execute_db(sql, self.db_conn, 'select')
        return res

    def set_hanle_over(self, source_id):
        sql = "UPDATE t_joom_source_products SET flag=1 WHERE id=%s;" % source_id
        execute_db(sql, self.db_conn, 'update')

    def delete_info(self):
        sql = "DELETE FROM t_joom_source_products WHERE flag=1;"
        execute_db(sql, self.db_conn, 'delete')
