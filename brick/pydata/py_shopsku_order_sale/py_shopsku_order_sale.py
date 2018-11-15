# -*- coding: utf-8 -*-

import logging
import pymssql
import datetime
from django.db import connection

logger = logging.getLogger('django.brick.pydata.py_shopsku_order_sale.py_shopsku_order_sale')

PYDB = {
    'host': '122.226.216.10',
    'port': 18794,
    'user': 'fancyqube',
    'password': 'K120Esc1',
    'database': 'ShopElf',
    'charset': 'utf8',
}


class HandleShopSKUInfo(object):
    def __init__(self):
        self.sum_data = list()
        self.duplicate_key = list()

    def py_db_conn(self):
        res = {'code': -1, 'message': '', 'db_conn': ''}
        try:
            pyuanConn = pymssql.connect(
                host=PYDB['host'],
                port=PYDB['port'],
                user=PYDB['user'],
                password=PYDB['password'],
                database=PYDB['database'],
                charset=PYDB['charset'],
            )
            res['code'] = 0
            res['db_conn'] = pyuanConn
        except Exception as e:
            logger.error("[.] PY DB CONNCETION ERROR: \n%s" % e)
            res['message'] = repr(e)

        return res

    def handle_db_data(self, data):
        start_time = datetime.datetime.now()
        logger.info("[.] handle_db_data start_time: %s" % start_time)
        source_data = list()
        now = datetime.datetime.now()
        for info in data:
            db_data_info = dict()
            orderday = info[0]
            shopname = info[1]
            shopsku = info[2]
            productsku = info[3]
            orders = int(info[4])
            sales = int(info[5])
            db_data_info = (orderday, shopname, shopsku, productsku, orders, sales, now, orders, sales, now)
            # db_data_info = (orderday, shopname, shopsku, productsku, orders, sales, now)
            source_data.append(db_data_info)

            # key = str(orderday) + '#@#' + str(shopname) + '#@#' + str(shopsku)
            # if key not in self.sum_data:
            #     self.sum_data.append(key)
            # else:
            #     logger.error("[.] =========== duplicate key: %s" % key)
            #     self.duplicate_key.append(key)

        end_time = datetime.datetime.now()
        logger.info("[.] handle_db_data end_time: %s" % end_time)
        handle_time = (end_time - start_time).total_seconds()
        logger.info("[.] handle_db_data handle_time: %s" % handle_time)

        return source_data

    def handle_source_data(self, py_conn_res):
        logger.info("[.] Start To Select ShopSKU Info.")

        pydb_conn = py_conn_res['db_conn']
        pydb_cursor = pydb_conn.cursor()

        sql = "SELECT CONVERT(VARCHAR(10), b.ordertime, 120) AS orderday, b.suffix, a.ebaysku AS shopsku, a.sku, COUNT(b.nid) AS ordernum, " \
            "SUM(a.l_qty) AS skusales FROM P_TradeDt a INNER JOIN P_Trade b ON b.nid = a.tradenid WHERE b.ordertime < %s " \
            "GROUP BY CONVERT(varchar(10), b.ordertime, 120), b.suffix, a.ebaysku, a.sku;"

        today = datetime.datetime.today().strftime('%Y-%m-%d')
        start_time = datetime.datetime.now()
        pydb_cursor.execute(sql, (today, ))
        # db_data = pydb_cursor.fetchall()
        end_time = datetime.datetime.now()
        handle_time = "%.3f" % (end_time - start_time).total_seconds()
        logger.debug("(%s) %s args('%s')" % (handle_time, sql, today))

        db_data = list()
        sRes = {'code': -1, 'message': ''}
        data = pydb_cursor.fetchone()
        all_num = 0
        start_get_time = datetime.datetime.now()
        logger.info("[.] get_ten_thousand_db_data start_get_time: %s" % start_get_time)
        while data:
            db_data.append(data)
            data = pydb_cursor.fetchone()
            if len(db_data) == 10000 or not data:
                all_num += len(db_data)

                end_get_time = datetime.datetime.now()
                logger.info("[.] get_ten_thousand_db_data end_get_time: %s" % end_get_time)
                handle_time = (end_get_time - start_get_time).total_seconds()
                logger.info("[.] get_ten_thousand_db_data handle_time: %s" % handle_time)

                source_data = self.handle_db_data(db_data)
                sRes = self.handle_data_process(source_data)
                logger.info("[.] Now Running All Numbers: %s" % all_num)
                db_data = list()
                if sRes['code'] != 0:
                    break
                start_get_time = datetime.datetime.now()
                logger.info("[.] get_ten_thousand_db_data start_get_time: %s" % start_get_time)
            if all_num == 10 * 10000:
                break

        logger.info("[.] Running All Numbers: %s" % all_num)

        # logger.error("[.] ALL Duplicate Key Numbers: %s" % len(self.duplicate_key))
        # logger.error("[.] ALL Duplicate Key: \n%s" % self.duplicate_key)

        pydb_cursor.close()
        pydb_conn.close()

        return sRes

    def update_shopsku_info(self, db_data):
        db_cursor = connection.cursor()

        start_time = datetime.datetime.now()
        logger.info("[.] update_shopsku_info start_time: %s" % start_time)

        sql = "INSERT INTO py_db.py_shopsku_info_test (OrderDay, ShopName, ShopSKU, ProductSKU, OrderNum, SaleNum, LastUpdateDate) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE " \
            "OrderNum=%s, SaleNum=%s, LastUpdateDate=%s;"

        # sql = "INSERT INTO py_db.py_shopsku_info_test (OrderDay, ShopName, ShopSKU, ProductSKU, OrderNum, SaleNum, LastUpdateDate) " \
        #     "VALUES (%s, %s, %s, %s, %s, %s, %s);"

        db_cursor.executemany(sql, db_data)
        db_cursor.execute('commit')

        db_cursor.close()

        end_time = datetime.datetime.now()
        logger.info("[.] update_shopsku_info end_time: %s" % end_time)
        handle_time = (end_time - start_time).total_seconds()
        logger.info("[.] update_shopsku_info handle_time: %s" % handle_time)

    def handle_data_process(self, source_data):
        sRes = {'code': -1, 'message': ''}

        try:
            self.update_shopsku_info(source_data)
            sRes['code'] = 0
        except Exception as e:
            sRes['message'] = 'update_shopsku_info error: %s' % repr(e)
            return sRes

        return sRes

    def clear_table(self):
        db_cursor = connection.cursor()
        # sql = "TRUNCATE TABLE py_db.py_shopsku_info;"
        sql = "TRUNCATE TABLE py_db.py_shopsku_info_test;"
        db_cursor.execute(sql)
        db_cursor.close()

    def py_shopsku_order_sale(self):
        sRes = {'code': -1, 'message': ''}
        py_conn_res = self.py_db_conn()
        if py_conn_res['code'] != 0:
            sRes['message'] = py_conn_res['message']
            return sRes

        # try:
        #     self.clear_table()
        #     logger.info("[.] Clear Table py_db.py_shopsku_info Over.")
        # except Exception as e:
        #     sRes['message'] = 'Clear Table py_db.py_shopsku_info Failed, Error Info: %s' % repr(e)
        #     return sRes

        try:
            sRes = self.handle_source_data(py_conn_res)
        except Exception as e:
            sRes['message'] = 'handle_source_data error: %s' % repr(e)
            return sRes

        return sRes
