# coding=utf-8

"""
author: szc
description: 生成WISH店铺每周(UTC时间)的订单数和销售额
"""

def connnect2Mysql():
    """
        连接MySQL数据库
        返回值：MySQL连接
    """
    import MySQLdb, time
    # HOST = 'hequskuapp.mysql.rds.aliyuncs.com'
    HOST = 'rm-uf6kd5a4wee2n2ze6o.mysql.rds.aliyuncs.com'
    PORT = 3306
    USER = 'by15161458383'
    PASSWORD = 'K120Esc1'
    DB = 'hq_db'
    CHARSET = 'utf8'
    try:
        mysqlClient = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB, charset=CHARSET)
        print 'connect to mysql'
    except MySQLdb.Error, e:
        print '38------------MySQL Error:%s，30秒后重新连接……' % str(e)
        time.sleep(30)
    return mysqlClient


class WishShopOrderSales(object):

    def __init__(self, cur):
        self.cur = cur

    def get_statistics(self):
        statistics_dict = {}
        sql1 = "select DATE_ADD(LastWeekStart, INTERVAL + 7 day),  DATE_ADD(LastWeekStart, INTERVAL + 14 day) from t_upload_shopname WHERE LastWeekStart is not null ORDER BY LastWeekStart DESC LIMIT 1; "
        sql2 = "select ShopName, count(1) as OrderNumber, ROUND(sum((Price+Shipping)*Quantity), 2) as SalesVolume from t_order WHERE OrderDate >= %s AND OrderDate < %s GROUP BY ShopName"
        sql3 = 'select id, ShopName, AllOrderNumber, AllSalesVolume from t_upload_shopname'
        self.cur.execute(sql1)
        date_infos = self.cur.fetchall()

        if date_infos:
            week_start = date_infos[0][0]
            week_end = date_infos[0][1]

            self.cur.execute(sql2, (week_start, week_end))
            statistics_infos = self.cur.fetchall()
            for statistics_info in statistics_infos:
                shop_name = statistics_info[0]
                order_number = int(statistics_info[1])
                sales_volume = statistics_info[2]
                statistics_dict[shop_name] = {'order_number': order_number, 'sales_volume': sales_volume}

            self.cur.execute(sql3)
            shopname_infos = self.cur.fetchall()

            return week_start, statistics_dict, shopname_infos
        else:
            return None, None, None


    def process_details(self, week_start, statistics_dict, shopname_infos):
        for shopname_info in shopname_infos:
            id = int(shopname_info[0])
            shop_name = shopname_info[1]
            all_order_number = eval(shopname_info[2]) if shopname_info[2] else {}
            all_sales_volume = eval(shopname_info[3]) if shopname_info[3] else {}
            last_order_number = statistics_dict.get(shop_name, {}).get('order_number', 0)
            last_sales_volume = statistics_dict.get(shop_name, {}).get('sales_volume', 0)
            all_order_number[week_start] = last_order_number
            all_sales_volume[week_start] = last_sales_volume
            param = (last_order_number, last_sales_volume, str(all_order_number), str(all_sales_volume), week_start, id)
            self.update_upload(param)


    def update_upload(self, param):
        sql = 'update t_upload_shopname set LastOrderNumber=%s, LastSalesVolume=%s, AllOrderNumber=%s, AllSalesVolume=%s, LastWeekStart=%s, UpdateTime=NOW() WHERE id=%s'
        self.cur.execute(sql, param)
        self.cur.execute('commit;')


if __name__ == "__main__":
    client = connnect2Mysql()
    cur = client.cursor()

    obj = WishShopOrderSales(cur)
    week_start, statistics_dict, shopname_infos = obj.get_statistics()
    obj.process_details(week_start, statistics_dict, shopname_infos)

    cur.close()
    client.close()