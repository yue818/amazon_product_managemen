# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: classskuableornot.py
 @time: 2018-01-06 11:20

"""
from brick.classredis.classsku import classsku
from brick.classredis.classmainsku import classmainsku
# judgeskuableornot

class classskuableornot():
    def __init__(self,db_conn=None,redis_conn=None):
        self.db_conn    = db_conn
        self.redis_conn = redis_conn

    def __private_base_judge_tort(self,sku,platform):
        #判断子SKU状态
        classsku_obj = classsku(self.db_conn,self.redis_conn)
        goodsstatus = classsku_obj.get_goodsstatus_by_sku(sku)
        if goodsstatus is None or goodsstatus.strip() != u'正常':
            return False

        #判断是否侵权
        classmainsku_obj = classmainsku(self.db_conn,self.redis_conn)
        mainsku = classsku_obj.get_bemainsku_by_sku(sku)
        skutort = None
        if mainsku is not None and mainsku.strip() != '':
            skutort = classmainsku_obj.get_tort_by_mainsku(mainsku)
        if skutort is not None and platform in skutort:
            return False
        else:
            return True

    def judgeskuableornotWish(self,sku):
        result = self.__private_base_judge_tort(sku,u'Wish')
        return result

    def judgeskuableornotAliexpress(self,sku):
        result = self.__private_base_judge_tort(sku,u'Aliexpress')
        return result

    def judgeskuableornoteBayUS(self,sku):
        result = self.__private_base_judge_tort(sku,u'eBay美国')
        return result

    def judgeskuableornoteBayEUR(self,sku):
        result = self.__private_base_judge_tort(sku,u'eBay欧洲')
        return result

    def judgeskuableornoteBayOther(self,sku):
        result = self.__private_base_judge_tort(sku,u'eBay其他')
        return result

    def judgeskuableornotAmazonUS(self,sku):
        result = self.__private_base_judge_tort(sku,u'Amazon美国')
        return result

    def judgeskuableornotAmazonEUR(self,sku):
        result = self.__private_base_judge_tort(sku,u'Amazon欧洲')
        return result

    def judgeskuableornotAmazonOther(self,sku):
        result = self.__private_base_judge_tort(sku,u'Amazon其他')
        return result
