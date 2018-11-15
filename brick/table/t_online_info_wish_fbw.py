#-*-coding:utf-8-*-
u"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: t_online_info_wish_fbw.py
 @time: 2018/9/3 15:21
"""


class t_online_info_wish_fbw():
    def __init__(self, connection):
        self.connection = connection

    def insert(self, param):
        try:
            sql = "insert into t_online_info_wish_fbw set product_id=%s,shopsku=%s,online_stock=%s," \
                  "demand_stock=%s,warehouse_code=%s,of_sales=%s,deliver_stock=%s,goodsshipping=%s " \
                  " on duplicate KEY update " \
                  " online_stock=%s,demand_stock=%s,of_sales=%s,deliver_stock=%s,goodsshipping=%s ;"
            cursor = self.connection.cursor()
            cursor.execute(sql, (param['product_id'],param['shopsku'],param['online_stock'],
                                 param['demand_stock'],param['warehouse_code'],param['of_sales'],
                                 param['deliver_stock'],param['goodsshipping'],
                                 #-------------------------------------------
                                 param['online_stock'],param['demand_stock'],param['of_sales'],
                                 param['deliver_stock'],param['goodsshipping'],))
            cursor.execute('commit;')
            cursor.close()
            return {'errorcode': 1}
        except Exception as error:
            return {'errorcode': -1, 'errortext': u'{}'.format(error)}


    def select_some_infor(self, product_id, shopsku, warehousename):
        try:
            sql = "select online_stock, demand_stock, of_sales,deliver_stock,goodsshipping from t_online_info_wish_fbw " \
                  "WHERE product_id=%s and shopsku=%s and warehouse_code=%s ;"

            cursor = self.connection.cursor()
            cursor.execute(sql, (product_id, shopsku, warehousename))
            obj = cursor.fetchone()
            cursor.close()
            if obj and (obj[0] or obj[1] or obj[2] or obj[3] or obj[4]):
                datadict = {
                    'online_stock': obj[0],'demand_stock': obj[1],
                    'of_sales':obj[2],'deliver_stock':obj[3],'goodsshipping':obj[4]
                }
                return {'errorcode': 1, 'datadict': datadict}
            else:
                return {'errorcode': 0, 'datadict': {}}
        except Exception as error:
            return {'errorcode': -1, 'errortext': u'{}'.format(error)}
















