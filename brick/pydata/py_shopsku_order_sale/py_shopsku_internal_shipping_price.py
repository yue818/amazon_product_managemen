# -*- coding: utf-8 -*-

import MySQLdb
import pymssql
import datetime
import logging
import logging.handlers
# from django.db import connection

# logger = logging.getLogger('django.brick.pydata.py_shopsku_order_sale')

log_formatter = logging.Formatter('%(asctime)s [%(filename)s %(funcName)s:%(lineno)d] %(thread)d %(levelname)s %(message)s')
logFile = 'ShopSKUInternalShippingPrice.log'
my_handler = logging.handlers.RotatingFileHandler(
    logFile,
    mode='a',
    maxBytes=100 * 1024 * 1024,
    backupCount=4,
    encoding=None,
    delay=0)

my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

logger = logging.getLogger('root')
logger.setLevel(logging.INFO)

# Print out log to the console
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

logger.addHandler(my_handler)
logger.addHandler(ch)

DATABASES = {
    'mysql': {
        'PORT': 3306,
        'NAME': 'report_db',
        'HOST': 'hequskuapp.mysql.rds.aliyuncs.com',
        'USER': 'by15161458383',
        'PASSWORD': 'K120Esc1',
    },
    'sqlserver': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ShopElf',
        'HOST': '122.226.216.10',
        'PORT': '18793',
        'USER': 'fancyqube',
        'PASSWORD': 'K120Esc1',
        'CHARSET': 'utf8',
    },
}


class ShopSKUInternalShippingPrice():
    def __init__(self, start_day, end_day):
        # self.db_conn = connection
        self.db_conn = MySQLdb.connect(
            user=DATABASES['mysql']['USER'],
            passwd=DATABASES['mysql']['PASSWORD'],
            host=DATABASES['mysql']['HOST'],
            db=DATABASES['mysql']['NAME'],
            port=DATABASES['mysql']['PORT'],
            charset='utf8'
        )
        self.pyuanConn = pymssql.connect(
            host=DATABASES['sqlserver']['HOST'],
            port=DATABASES['sqlserver']['PORT'],
            user=DATABASES['sqlserver']['USER'],
            password=DATABASES['sqlserver']['PASSWORD'],
            database=DATABASES['sqlserver']['NAME'],
            charset=DATABASES['sqlserver']['CHARSET'],
        )
        self.start_day = start_day
        self.end_day = end_day

    def close_mysql(self):
        self.db_conn.close()

    def close_sqlserver(self):
        self.pyuanConn.close()

    def handle_sum_purchase_info_price(self, db_data=None, isp_db_data=None, pss_db_data=None):
        logger.info("[.] handle_sum_purchase_info_price")
        data_info = dict()

        if db_data:
            for i in db_data:
                if i[0] not in data_info.keys():
                    data_info[i[0]] = dict()
                data_info[i[0]]['InternalShippingPrice'] = i[1]
                data_info[i[0]]['DayAllMoney'] = i[2]
        else:
            for i in isp_db_data:
                if i[0] not in data_info.keys():
                    data_info[i[0]] = dict()
                    data_info[i[0]]['DayAllMoney'] = 0
                data_info[i[0]]['InternalShippingPrice'] = i[1]

            for i in pss_db_data:
                if i[0] not in data_info.keys():
                    data_info[i[0]] = dict()
                    data_info[i[0]]['InternalShippingPrice'] = 0
                data_info[i[0]]['DayAllMoney'] = i[1]

        return data_info

    def get_sum_purchase_info_price(self):
        logger.info("[.] get_sum_purchase_info_price")
        pydb_cursor = self.pyuanConn.cursor()

        # isp_sql = "SELECT CONVERT(VARCHAR(10), MakeDate, 120) AS OrderDay, SUM(expressfee) AS InternalShippingPrice FROM " \
        #     "ShopElf.dbo.CG_StockOrderM GROUP BY CONVERT(VARCHAR(10), MakeDate, 120);"

        # pss_sql = "SELECT CONVERT(VARCHAR(10), a.MakeDate, 120) AS OrderDay, SUM(b.allmoney) AS DayAllMoney " \
        #     "FROM ShopElf.dbo.CG_StockOrderM a INNER JOIN ShopElf.dbo.CG_StockOrderD b ON a.NID = b.stockordernid " \
        #     "GROUP BY CONVERT(VARCHAR(10), a.MakeDate, 120) ORDER BY CONVERT(VARCHAR(10), a.MakeDate, 120) DESC;"

        # pydb_cursor.execute(isp_sql)
        # isp_db_data = pydb_cursor.fetchall()
        # pydb_cursor.execute(pss_sql)
        # pss_db_data = pydb_cursor.fetchall()
        # sum_purchase_info_price = self.handle_sum_purchase_info_price(isp_db_data=isp_db_data, pss_db_data=pss_db_data)

        sql = "SELECT CONVERT(VARCHAR(10), a.MakeDate, 120) AS OrderDay, SUM(a.expressfee) AS InternalShippingPrice, SUM(b.allmoney) AS DayAllMoney " \
            "FROM ShopElf.dbo.CG_StockOrderM a INNER JOIN (select stockordernid,sum(allmoney) AS allmoney from ShopElf.dbo.CG_StockOrderD " \
            "GROUP BY stockordernid ) b ON a.NID = b.stockordernid " \
            "WHERE CONVERT(VARCHAR(10), a.MakeDate, 120)>=%s AND CONVERT(VARCHAR(10), a.MakeDate, 120)<%s " \
            "GROUP BY CONVERT(VARCHAR(10), a.MakeDate, 120) ORDER BY CONVERT(VARCHAR(10), a.MakeDate, 120) DESC;"

        pydb_cursor.execute(sql, (self.start_day, self.end_day))
        db_data = pydb_cursor.fetchall()
        sum_purchase_info_price = self.handle_sum_purchase_info_price(db_data=db_data)

        pydb_cursor.close()

        return sum_purchase_info_price

    def handle_sum_sales_info(self, db_data):
        logger.info("[.] handle_sum_sales_info")
        data_info = dict()

        for i in db_data:
            if i[0] not in data_info.keys():
                data_info[i[0]] = dict()
            data_info[i[0]]['day_sum_sales'] = i[1]
            data_info[i[0]]['day_sum_numbers'] = i[2]
            data_info[i[0]]['day_sum_weight'] = i[3]
            data_info[i[0]]['day_sum_internal_shipping_price'] = 0
            data_info[i[0]]['day_sum_purchase_info_price'] = 0

        return data_info

    def get_sum_sales_info(self):
        logger.info("[.] get_sum_sales_info")
        sql = "SELECT CLOSINGDATE, SUM(SaleVolume), SUM(SaleNum), SUM(weight*SaleNum) FROM report_db.t_saler_profit_report_dd " \
            "WHERE CLOSINGDATE >= %s AND CLOSINGDATE < %s GROUP BY CLOSINGDATE;"

        mysql_cursor = self.db_conn.cursor()
        mysql_cursor.execute(sql, (self.start_day, self.end_day))
        db_data = mysql_cursor.fetchall()
        sum_sale_info = self.handle_sum_sales_info(db_data)
        mysql_cursor.close()

        return sum_sale_info

    def handle_shopsku_day_weight(self, db_data):
        logger.info("[.] handle_shopsku_day_weight")
        data_info = dict()

        for i in db_data:
            if i[0] not in data_info.keys():
                data_info[i[0]] = list()
            data_w = dict()
            data_w['ShopSKU'] = i[1]
            data_w['ProductSKU'] = i[2]
            data_w['ShopName'] = i[3]
            data_w['weight'] = i[4]
            data_w['l_number'] = i[5]
            data_info[i[0]].append(data_w)

        return data_info

    def get_shopsku_day_weight(self):
        logger.info("[.] get_shopsku_day_weight")
        sql = "SELECT CLOSINGDATE, ShopSKU, ProductSKU, suffix, weight*SaleNum as sumweight, l_number FROM report_db.t_saler_profit_report_dd " \
            "WHERE tradetype!='advertising' AND CLOSINGDATE >= %s AND CLOSINGDATE < %s;"

        mysql_cursor = self.db_conn.cursor()
        mysql_cursor.execute(sql, (self.start_day, self.end_day))
        db_data = mysql_cursor.fetchall()
        shopsku_day_weight = self.handle_shopsku_day_weight(db_data)
        del db_data
        mysql_cursor.close()

        return shopsku_day_weight

    def handle_day_sum_info(self, sum_purchase_info_price, sum_sales_info, shopsku_day_weight):
        logger.info("[.] handle_day_sum_info")
        for day in sum_purchase_info_price.keys():
            if day not in sum_sales_info.keys():
                sum_sales_info[day] = dict()
                sum_sales_info[day]['day_sum_weight'] = 0
                sum_sales_info[day]['day_sum_sales'] = 0
                sum_sales_info[day]['day_sum_numbers'] = 0
            sum_sales_info[day]['day_sum_internal_shipping_price'] = sum_purchase_info_price[day].get('InternalShippingPrice', 0)
            sum_sales_info[day]['day_sum_purchase_info_price'] = sum_purchase_info_price[day].get('DayAllMoney', 0)

        for day in shopsku_day_weight.keys():
            sum_weight = 0
            for i in shopsku_day_weight[day]:
                sum_weight += i['weight']

            if day not in sum_sales_info.keys():
                sum_sales_info[day] = dict()
                sum_sales_info[day]['day_sum_sales'] = 0
                sum_sales_info[day]['day_sum_numbers'] = 0
                sum_sales_info[day]['day_sum_internal_shipping_price'] = 0
                sum_sales_info[day]['day_sum_weight'] = sum_weight

        return sum_sales_info

    def handle_shopsku_internal_shipping_price(self):
        logger.info("[.] handle_shopsku_internal_shipping_price")
        sum_purchase_info_price = self.get_sum_purchase_info_price()
        sum_sales_info = self.get_sum_sales_info()
        shopsku_day_weight = self.get_shopsku_day_weight()

        day_sum_info = self.handle_day_sum_info(sum_purchase_info_price, sum_sales_info, shopsku_day_weight)

        for day in shopsku_day_weight.keys():
            day_sum_internal_shipping_price = float(sum_purchase_info_price.get(day, {}).get('InternalShippingPrice', 0))
            day_sum_weight = float(day_sum_info.get(day, {}).get('day_sum_weight', 0))
            if not day_sum_weight or not day_sum_internal_shipping_price:
                for info in shopsku_day_weight[day]:
                    info['InternalShippingPrice'] = 0
            else:
                for info in shopsku_day_weight[day]:
                    sp = float(info['weight']) / day_sum_weight * day_sum_internal_shipping_price
                    info['InternalShippingPrice'] = sp

        return shopsku_day_weight, day_sum_info

    def handle_result_data(self, data):
        logger.info("[.] handle_result_data")
        result_data = list()
        now = datetime.datetime.now()
        for day in data.keys():
            for info in data[day]:
                source_data = (
                    info['InternalShippingPrice'], now, day, info['ShopName'], info['ShopSKU'],
                    info['ProductSKU'], info['l_number'], self.start_day, self.end_day
                )
                result_data.append(source_data)

        return result_data

    def handle_day_sum_info_to_db(self, day_sum_info):
        logger.info("[.] handle_day_sum_info_to_db")
        result_data = list()
        now = datetime.datetime.now()
        for day in day_sum_info.keys():
            source_data = (
                day, day_sum_info[day].get('day_sum_weight', 0), None, day_sum_info[day].get('day_sum_sales', 0),
                day_sum_info[day].get('day_sum_purchase_info_price', 0), day_sum_info[day].get('day_sum_numbers', 0),
                day_sum_info[day].get('day_sum_internal_shipping_price', 0), now,
                day_sum_info[day].get('day_sum_weight', 0), None, day_sum_info[day].get('day_sum_sales', 0),
                day_sum_info[day].get('day_sum_purchase_info_price', 0), day_sum_info[day].get('day_sum_numbers', 0),
                day_sum_info[day].get('day_sum_internal_shipping_price', 0), now
            )
            result_data.append(source_data)

        return result_data

    def update_general_db_info(self, result_data):
        logger.info("[.] update_general_db_info")
        mysql_cursor = self.db_conn.cursor()

        sql = "UPDATE report_db.t_saler_profit_report_dd SET InternalShippingPrice=%s, ISPLastUpdateDate=%s WHERE CLOSINGDATE=%s AND " \
            "suffix=%s AND ShopSKU=%s AND ProductSKU=%s AND l_number=%s AND tradetype!='advertising' AND CLOSINGDATE >= %s AND CLOSINGDATE < %s;"

        num = len(result_data) / 10000 + 1
        for i in range(num):
            start_num = i * 10000
            logger.info('[.] start_num: %s' % start_num)
            end_num = (i + 1) * 10000
            logger.info('[.] end_num: %s' % end_num)
            mysql_cursor.executemany(sql, result_data[start_num:end_num])
            # if i == 2:
            #     break
        mysql_cursor.execute('commit;')

        mysql_cursor.close()

    def update_detaild_db_info(self, result_sum_data):
        logger.info("[.] update_detaild_db_info")
        mysql_cursor = self.db_conn.cursor()

        sum_sql = "INSERT INTO report_db.py_shopsku_internal_shipping_price (OrderDay, SaleSumWeight, PurchaseSumWeight, SaleSumPrice, " \
            "PurchaseSumPrice, SaleSumNumbers, InternalShippingPrice, LastUpdateDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE " \
            "SaleSumWeight=%s, PurchaseSumWeight=%s, SaleSumPrice=%s, PurchaseSumPrice=%s, SaleSumNumbers=%s, InternalShippingPrice=%s, LastUpdateDate=%s;"

        mysql_cursor.executemany(sum_sql, result_sum_data)
        mysql_cursor.execute('commit;')

        mysql_cursor.close()

    def clear_detail_table(self):
        logger.info("[.] TRUNCATE TABLE report_db.py_shopsku_internal_shipping_price;")
        mysql_cursor = self.db_conn.cursor()
        sql = "TRUNCATE TABLE report_db.py_shopsku_internal_shipping_price;"
        mysql_cursor.execute(sql)
        mysql_cursor.close()

    def clear_general_table(self):
        mysql_cursor = self.db_conn.cursor()
        general_clean_sql = "UPDATE report_db.t_saler_profit_report_dd SET InternalShippingPrice=NULL, ISPLastUpdateDate=NULL " \
            "WHERE CLOSINGDATE >= %s AND CLOSINGDATE < %s;"
        mysql_cursor.execute(general_clean_sql, (self.start_day, self.end_day))
        mysql_cursor.execute('commit;')
        logger.info("[.] %s" % (general_clean_sql % (self.start_day, self.end_day)))
        mysql_cursor.close()

    def main_process(self):
        # self.clear_detail_table()
        self.clear_general_table()
        data, day_sum_info = self.handle_shopsku_internal_shipping_price()
        result_data = self.handle_result_data(data)
        self.update_general_db_info(result_data)
        result_sum_data = self.handle_day_sum_info_to_db(day_sum_info)
        self.update_detaild_db_info(result_sum_data)
        self.close_mysql()
        self.close_sqlserver()


# if __name__ == '__main__':
def main_fun():
    day_range = [
        # ('2018-03-01', '2018-04-01'),
        # ('2018-04-01', '2018-05-01'),
        # ('2018-05-01', '2018-06-01'),
        # ('2018-06-01', '2018-07-01'),
        # ('2018-07-01', '2018-08-01'),
        # ('2018-08-01', '2018-09-01'),
        ('2018-09-01', '2018-10-01'),
        # ('2018-10-01', '2018-11-01'),
    ]
    all_start_time = datetime.datetime.now()
    logger.info("[x] [%s] Start To Run ShopSKUInternalShippingPrice." % all_start_time)
    for day in day_range:
        month_start_time = datetime.datetime.now()
        logger.info("[.] [%s] Start To Run %s to %s Infos" % (month_start_time, day[0], day[1]))
        main_obj = ShopSKUInternalShippingPrice(day[0], day[1])
        main_obj.main_process()
        month_end_time = datetime.datetime.now()
        logger.info("[.] [%s] End To Run %s to %s Infos" % (month_end_time, day[0], day[1]))
        handle_time = (month_end_time - month_start_time).total_seconds()
        logger.info("[.] Handle Run %s to %s Infos Of Time: %s." % (day[0], day[1], handle_time))
    all_end_time = datetime.datetime.now()
    logger.info("[x] [%s] End To Run ShopSKUInternalShippingPrice." % all_end_time)
    logger.info("[x] Handle ShopSKUInternalShippingPrice Time: %s." % (all_end_time - all_start_time).total_seconds())
