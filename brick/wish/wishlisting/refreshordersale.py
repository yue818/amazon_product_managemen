# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: refreshordersale.py
 @time: 2017-12-22 9:16

"""
from brick.table.t_report_orders1days import t_report_orders1days
from brick.table.t_order import t_order




def run(params):
    t_report_orders1days_obj = t_report_orders1days(params['dbcnxn'])
    t_report_orders1days_obj.deletedata_befor60day(params['ProductID'])  # 删除 (普通仓) 60天以前数据

    t_order_obj = t_order(params['ShopName'],params['dbcnxn'])

    warehouse_list = ['STANDARD', 'US', 'GB', 'DE', 'FBW']

    for warehouse in warehouse_list:
        objs = t_order_obj.get_order_data_by_productid(params['ProductID'],warehouse)
        for obj in objs:
            if obj:
                insertintodict = {}

                insertintodict['WarehouseName']   = warehouse
                if warehouse == 'FBW':  # FBW
                    insertintodict['WarehouseName'] = "{}-{}".format(warehouse, obj[4])

                insertintodict['ProductID']       = obj[0] # productid
                insertintodict['YYYYMMDD']        = obj[1]

                insertintodict['OrdersLast1Days'] = 0
                if obj[2] is not None:
                    insertintodict['OrdersLast1Days'] = int(obj[2])

                insertintodict['UpdateTime']      = obj[3].strftime('%Y-%m-%d')

                insertintodict['ShopName']        = params['ShopName']

                insertintodict['PlatformName']    = params['ShopName'].split('-')[0]  # Wish-

                if warehouse == 'STANDARD':  # 普通仓7天订单数
                    insertintodict['OrdersLast7Days'] = t_report_orders1days_obj.getOrders7Days(params['ProductID'],obj[1])
                    t_report_orders1days_obj.insertinto(insertintodict)

                else: # 海外仓7天订单数  fbw
                    insertintodict['OrdersLast7Days'] = t_report_orders1days_obj.getOrders7Days_WarehouseName(
                        params['ProductID'], obj[1], warehousename=warehouse
                    )
                    # print insertintodict
                    t_report_orders1days_obj.insertinto_WarehouseName(insertintodict)







# # 测试 新增字段
#
# from brick.db.dbconnect import run as runconn
#
# conn = runconn({})['db_conn']
# try:
#     cursor = conn.cursor()
#     cursor.execute("select DISTINCT ProductID, ShopName FROM t_order WHERE LEFT(OrderDate,10) >= date_format(DATE_ADD(utc_date(), INTERVAL -60 DAY), '%%Y-%%m-%%d');")
#     objs = cursor.fetchall()
#     cursor.close()
#
#     num = len(objs)
#     i = 0
#     for obj in objs:
#         print 'num====={},------i====={},----obj====={}'.format(num,i,obj)
#         param = {
#             'dbcnxn': conn,
#             'ShopName': obj[-1],
#             'ProductID': obj[0]
#         }
#
#         run(param)
#         i = i + 1
#
# except Exception as ex:
#     print ex
# conn.close()

