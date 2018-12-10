# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: test.py
 @time: 2018/12/6 10:44
"""


def test(name, age, **dict):
    print name
    print age
    print dict


test('name', 11, from_address={1: 1})


from_addr = dict()
from_addr['name'] = 'Anjun'  # 1
from_addr['address_1'] = 'Jiadingqu Antingzhen Xiechunlu 1300nong 3hao Aqu'  # 1
# from_addr['address_2'] = 'address_2'  # 0
from_addr['city'] = 'Shanghai'  # 1
# from_addr['district_or_county'] = 'district_or_county'  # 0
from_addr['state_or_province'] = 'Shanghai'  # 0
from_addr['postal_code'] = '201804'  # 0
from_addr['country'] = 'CN'  # 0


item_args = list()
item_each = dict()
# CreateInboundShipmentPlan
item_each['sku'] = 'sku'  # 1
item_each['quantity'] = 'quantity'  # 1
item_each['quantity_in_case'] = 'quantity_in_case'
item_each['asin'] = 'asin'
item_each['condition'] = 'condition'
# create_inbound_shipment, update_inbound_shipment
item_each['sku'] = 'sku'  # 1
item_each['quantity'] = 'quantity'  # 1
item_each['quantity_in_case'] = 'quantity_in_case'
