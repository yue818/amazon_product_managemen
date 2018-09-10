# -*- coding:utf-8 -*-

"""  
 @desc:  
 @author: wuchongxiang 
 @site: 
 @software: PyCharm
 @file: testa.py
 @time: 2018/8/16 10:11
"""
# shopsku = 'WVKCY1081*5+WVKCY1082'
# for shopskutmp in shopsku.split('+'):
#     newshopsku_list = shopskutmp.split('*')
#     print newshopsku_list
#     if len(newshopsku_list) == 1:
#         print newshopsku_list[0]
#     else:
#         print newshopsku_list[1]


def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we're all out of", kind)
    for arg in arguments:
        print(arg)
    print("-" * 40)
    for kw in keywords:
        print kw, ":", keywords[kw]


cheeseshop("Limburger", "It's very runny, sir.", "It's really very, VERY runny, sir.", shopkeeper= "Michael Palin", client= "John Cleese", sketch="Cheese Shop Sketch")