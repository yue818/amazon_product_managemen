# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: 20181113.py
 @time: 2018/11/13 17:36
"""  
product_info_dic ={"generic_keywords3": '', "generic_keywords2": '', "generic_keywords1": "1111111111111111111111111111111", "generic_keywords5": '', "generic_keywords4": '', "item_name": "Bohonan Test_for_VAR Black - Test1", "product_description": "222222", "bullet_point4": "2", "bullet_point5": "2", "bullet_point1": "2", "bullet_point2": "2", "bullet_point3": "2", "seller_sku": "_((!${:8645"}

set_sql = ''
where_sql = ''
for key, val in product_info_dic.items():
    if key == 'seller_sku':
        where_sql = key + '="' + val + '"'
    else:
        set_sql += key + '="' + val + '",'
print set_sql
print
print where_sql


bullet_point1 = ""
if bullet_point1:
    print 11
else:
    print 22