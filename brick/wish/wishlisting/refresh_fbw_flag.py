#-*-coding:utf-8-*-
u"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: refresh_fbw_flag.py
 @time: 2018/9/3 13:24
"""
from brick.table.t_stocking_demand_fbw import t_stocking_demand_fbw
from brick.table.t_order import t_order
from brick.table.t_online_info_wish_fbw import t_online_info_wish_fbw

def refresh_fbw_flag(product_id, shopsku, shopname, connection):
    warehousecode = [
        {'code': 'FBW-LAX', 'name': u'FBW-US-LAX (美国)', 'des': 'FBW-US', 'ware_code': 'LAX'},
        {'code': 'FBW-SF', 'name': u'SF Express (爱沙尼亚)', 'des': 'FBW-EU', 'ware_code': 'SF'},
        # {'code': 'FBW-CVG', 'name': u'FBW-US-CVG (美国)', 'des': 'FBW-US', 'ware_code': 'CVG'},
    ]

    t_stocking_demand_fbw_obj = t_stocking_demand_fbw(connection=connection)
    t_order_obj = t_order(shopname, connection)
    t_online_info_wish_fbw_obj = t_online_info_wish_fbw(connection)

    flag = 'False'

    for warecode in warehousecode:
        warehousename = warecode['code']  # 目前默认是美西仓 FBW-LAX

        of_sales = t_order_obj.fbw_shopsku_sales(product_id, shopsku, warecode['ware_code'])  # 下面获取销量  是销售数量 不是订单量
        if of_sales['errorcode'] == 1:
            flag = 'True'
        sales_num = int(of_sales['ofsales']) if of_sales['errorcode'] == 1 and of_sales['ofsales'] else 0

        demand_obj = t_stocking_demand_fbw_obj.getdemand_stock_num(
            product_id=product_id,shopsku=shopsku, shopname=shopname,warehouse=warecode['des']
        )

        if demand_obj['errorcode'] == -1:
            raise Exception(demand_obj['errortext'])
        elif demand_obj['errorcode'] == 0:
            stock_num = 0 - sales_num
        else:
            stock_num = int(demand_obj['deliver_stock']) - sales_num  # 发货量-售出量=在线库存
            flag = 'True'

        if flag == 'True':
            insert_param = {
                'product_id': product_id,
                'shopsku': shopsku,
                'online_stock': stock_num,
                'demand_stock': demand_obj.get('demand_stock', 0),
                'warehouse_code': warehousename,
                'of_sales': sales_num,
                'deliver_stock': demand_obj.get('deliver_stock', 0),
                'goodsshipping': of_sales.get('Shipping')
            }

            t_online_info_wish_fbw_obj.insert(insert_param)

    return flag



