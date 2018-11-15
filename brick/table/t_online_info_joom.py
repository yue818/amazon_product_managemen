# -*- coding: utf-8 -*-

from brick.db.dbconnect import execute_db


class t_online_info_joom():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_joom_products_by_productids(self, product_ids):
        joom_products = "SELECT ProductID, OfSales FROM t_online_info_joom WHERE ProductID IN (%s);" % product_ids
        joom_products_info = execute_db(joom_products, self.db_conn, 'select')
        return joom_products_info

    def set_joom_products_cut_price_status(self, products_id, status):
        joom_status = "UPDATE t_online_info_joom SET cutprice_flag=%s WHERE ProductID='%s'" % (status, products_id)
        res = execute_db(joom_status, self.db_conn, 'update')
        return res

    def set_joom_seven_orders(self, sevenorders, product_id):
        sql_orders = "UPDATE t_online_info_joom SET Orders7Days=%s WHERE ProductID='%s';" % (sevenorders, product_id)
        res = execute_db(sql_orders, self.db_conn, 'update')
        return res

    def set_joom_ratingvalue(self, product_id, ratingValue):
        sql_orders = "UPDATE t_online_info_joom SET ratingValue=%s WHERE ProductID='%s';" % (ratingValue, product_id)
        res = execute_db(sql_orders, self.db_conn, 'update')
        return res

    def refresh_joom_data(self, params):
        result = {}
        try:
            mycur = self.db_conn.cursor()
            sql = "INSERT INTO t_online_info_joom SET " \
                "PlatformName='Joom',ProductID=%s,ShopIP='',ShopName=%s,Title=%s,SKU=%s," \
                "ShopSKU=%s,Price=%s,Quantity=0,Orders7Days=%s,SoldYesterday=%s," \
                "SoldTheDay=%s,SoldXXX=%s,DateOfOrder=%s,RefreshTime=%s," \
                "Image=%s,Status=%s,ReviewState=%s,DateUploaded=%s,LastUpdated=%s,OfSales=%s," \
                "ParentSKU=%s,Seller=%s,TortInfo=%s,MainSKU=%s,DataSources=%s,OperationState=%s" \
                ",Published=%s,market_time=%s,is_promoted=%s,JoomExpress=%s ON DUPLICATE KEY UPDATE" \
                " Title=%s,Orders7Days=%s,SoldYesterday=%s," \
                "SoldTheDay=%s,SoldXXX=%s,DateOfOrder=%s,RefreshTime=%s,Status=%s," \
                "ReviewState=%s,DateUploaded=%s,LastUpdated=%s,OfSales=%s,Seller=%s," \
                "TortInfo=%s,MainSKU=%s,DataSources=%s,OperationState=%s,Published=%s," \
                "market_time=%s,ShopSKU=%s,is_promoted=%s,JoomExpress=%s;"
            mycur.execute(sql, (params['ProductID'], params['ShopName'], params['Title'], params['SKU'],
                                params['ShopSKU'], params['Price'], params['Orders7Days'], params['SoldYesterday'],
                                params['SoldTheDay'], params['SoldXXX'], params['DateOfOrder'], params['RefreshTime'],
                                params['Image'], params['Status'], params['ReviewState'], params['DateUploaded'],
                                params['LastUpdated'], params['OfSales'], params['ParentSKU'], params['Seller'],
                                params['TortInfo'], params['MainSKU'], params['DataSources'], params['OperationState'],
                                params['Published'], params['market_time'], params['is_promoted'], params['JoomExpress'],
                                params['Title'], params['Orders7Days'], params['SoldYesterday'], params['SoldTheDay'],
                                params['SoldXXX'], params['DateOfOrder'], params['RefreshTime'], params['Status'], params['ReviewState'],
                                params['DateUploaded'], params['LastUpdated'], params['OfSales'], params['Seller'],
                                params['TortInfo'], params['MainSKU'], params['DataSources'], params['OperationState'],
                                params['Published'], params['market_time'], params['ShopSKU'], params['is_promoted'], params['JoomExpress'],))
            mycur.execute("commit;")
            mycur.close()
            result['code'] = 0
            result['error'] = ''
        except Exception, ex:
            result['code'] = 1
            result['error'] = '%s:%s' % (Exception, ex)
        return result
