#-*-coding:utf-8-*-
u"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_stocking_demand_fbw.py
 @time: 2018/9/3 11:15
"""
class t_stocking_demand_fbw():
    def __init__(self, connection):
        self.connection = connection

    def getdemand_stock_num(self,product_id, shopsku, shopname, warehouse):
        try:
            sql1 = "select SUM(QTY) from t_stocking_demand_fbw " \
                  "where ProductID=%s and ShopSKU=%s and AccountNum=%s and `Status` <> 'nodemand' " \
                  "and Destination_warehouse=%s GROUP BY ShopSKU;"
            cursor = self.connection.cursor()
            cursor.execute(sql1, (product_id, shopsku, shopname, warehouse))
            obj1 = cursor.fetchone()
            qty = int(obj1[0]) if obj1 and obj1[0] else 0

            sql2 = "select SUM(QTY) from t_stocking_demand_fbw " \
                  "where ProductID=%s and ShopSKU=%s and AccountNum=%s and `Status` = 'deliver' " \
                  "and Destination_warehouse=%s GROUP BY ShopSKU;"
            cursor.execute(sql2, (product_id, shopsku, shopname, warehouse))
            obj2 = cursor.fetchone()
            deliver_stock = int(obj2[0]) if obj2 and obj2[0] else 0

            cursor.close()
            if qty > 0:
                return {'errorcode': 1, 'demand_stock': qty - deliver_stock, 'deliver_stock': deliver_stock}
            else:
                return {'errorcode': 0}
        except Exception as error:
            return {'errorcode': -1, 'errortext': u'{}'.format(error)}





