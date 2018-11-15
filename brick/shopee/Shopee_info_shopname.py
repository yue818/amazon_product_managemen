# -*- coding:utf-8 -*-

"""
 @desc:
 @author: 张浩
 @site:
"""

from django_redis import get_redis_connection
from shopee_app.table.t_config_online_shopee import t_config_online_shopee

def get_shopee_info(shopname):
    # 获取店铺信息
    shopee_info = t_config_online_shopee.objects.filter(ShopName=shopname).values('K', 'V')
    partner_id = ''
    shopid = ''
    for s in shopee_info:
        if s['K'] == 'partner_id':
            partner_id = s['V']
        if s['K'] == 'shopid':
            shopid = s['V']
    shopee_dict = dict()
    shopee_dict['partner_id'] = partner_id
    shopee_dict['shopid'] = shopid
    return shopee_dict

def get_AvailableNum(varid, itemid, SKU, VariationSKU):
    redis_conn = get_redis_connection(alias='product')
    pipe = redis_conn.pipeline(transaction=False)
    isNOs = [(varid, itemid, SKU, VariationSKU)]
    ids = []
    for obj in isNOs:
        ids.append((obj[0], obj[2], obj[3]))
        pipe.hget(obj[2],'Number')
        pipe.hget(obj[2],'ReservationNum')
        pipe.hget(obj[2],'CanSaleDay')
    result = pipe.execute()
    for i, dd in enumerate(ids):
        AvailableNum = (int(result[i*3]) if result[i*3] else 0) - (int(result[i*3+1]) if result[i*3+1] else 0)
        saleday = result[i*3+2]
    return (AvailableNum, saleday)
