# -*- coding: utf-8 -*-
"""
 @desc:
 @author: 李杨杨
 @site:
 @software: PyCharm
 @file: classmainsku.py
 @time: 2017-12-26 14:43

"""
class classmainsku():
    def __init__(self, db_cnxn=None, redis_cnxn=None):
        self.db_cnxn = db_cnxn
        self.redis_cnxn = redis_cnxn
    #公共方法
    def __private_set_attr(self,name,key,value):
        if self.redis_cnxn is not None and value is not None:
            self.redis_cnxn.hset(name, key,value)

    def __private_get_attr(self,name,key):
        if self.redis_cnxn is not None:
            return self.redis_cnxn.hget(name,key)


    # set子sku列表
    def set_sku_by_mainsku(self, mainsku, sku):
        return self.__private_set_attr(mainsku,'SKU',sku)

    # get子sku列表
    def get_sku_by_mainsku(self,mainsku):
        productsku = self.__private_get_attr(mainsku,'SKU')
        if productsku is None and self.db_cnxn is not None:
            skucur = self.db_cnxn.cursor()
            skucur.execute('select ProductSKU from t_product_mainsku_sku where MainSKU = %s ;',(mainsku,))
            objs = skucur.fetchall()
            skucur.close()
            productskulist = []
            for obj in objs:
                if obj and obj[0] is not None:
                    productskulist.append(obj[0])
            if len(productskulist) >= 1:
                productsku = '|'.join(productskulist)
                self.set_sku_by_mainsku(mainsku, productsku)
        if productsku is not None:
            productsku = productsku.split('|')
        return productsku


    # set 主sku名称
    def set_goodsname_by_mainsku(self, mainsku, goodsname):
        return self.__private_set_attr(mainsku, 'Name2', goodsname)

    # get 主sku名称
    def get_goodsname_by_mainsku(self,mainsku):
        goodsname = self.__private_get_attr(mainsku,'Name2')
        if goodsname is None and self.db_cnxn is not None:
            namecur = self.db_cnxn.cursor()
            namecur.execute('select Name2 from t_product_enter_ed where MainSKU = %s ;',(mainsku,))
            obj = namecur.fetchone()
            namecur.close()
            if obj:
                goodsname = obj[0]
                self.set_goodsname_by_mainsku(mainsku,goodsname)
        return goodsname


    # set 主图
    def set_mainpic_by_mainsku(self, mainsku, mainpic):
        return self.__private_set_attr(mainsku,'MainImage',mainpic)

    # get 主图
    def get_mainpic_by_mainsku(self,mainsku):
        return self.__private_get_attr(mainsku,'MainImage')



    # set 副图
    def set_extrapic_by_mainsku(self, mainsku, extrapic):
        return self.__private_set_attr(mainsku,'ExtraImages',extrapic)

    # get 副图
    def get_extrapic_by_mainsku(self,mainsku):
        return self.__private_get_attr(mainsku, 'ExtraImages')


    # set 开发时间
    def set_kftime_by_mainsku(self, mainsku, kftime):
        return self.__private_set_attr(mainsku,'KFTime',kftime)

    # get 开发时间
    def get_kftime_by_mainsku(self,mainsku):
        kftime = self.__private_get_attr(mainsku,'KFTime')
        if kftime is None and self.db_cnxn is not None:
            kftcur = self.db_cnxn.cursor()
            kftcur.execute('select KFTime from t_product_enter_ed where MainSKU = %s ;',(mainsku,))
            obj = kftcur.fetchone()
            kftcur.close()
            if obj:
                kftime = obj[0]
                self.set_kftime_by_mainsku(mainsku, kftime)
        return kftime


    # set 开发人
    def set_kfperson_by_mainsku(self, mainsku, kfperson):
        return self.__private_set_attr(mainsku, 'KFStaffName', kfperson)

    # get 开发人
    def get_kfperson_by_mainsku(self,mainsku):
        kfperson = self.__private_get_attr(mainsku,'KFStaffName')
        if kfperson is None and self.db_cnxn is not None:
            percur = self.db_cnxn.cursor()
            percur.execute('select KFStaffName from t_product_enter_ed where MainSKU = %s ;',(mainsku,))
            obj = percur.fetchone()
            percur.close()
            if obj and self.redis_cnxn is not None:
                kfperson = obj[0]
                self.set_kfperson_by_mainsku(mainsku, kfperson)
        return kfperson


    # set 侵权站点
    def set_tort_by_mainsku(self, mainsku,tort):
        return self.__private_set_attr(mainsku,'Site',tort)

    # get 侵权站点
    def get_tort_by_mainsku(self, mainsku):
        tort = self.__private_get_attr(mainsku, 'Site')
        if tort is None and self.db_cnxn is not None:
            percur = self.db_cnxn.cursor()
            percur.execute('select IPForbiddenSite from t_tort_info where MainSKU = %s and OperationState = "Y";', (mainsku,))
            objs = percur.fetchall()
            percur.close()
            tortlist = []
            for obj in objs:
                if obj and obj[0] is not None and obj[0].strip() != '':
                    if obj[0].strip() == 'All':
                        tortlist = tortlist + ['Wish', 'Aliexpress', 'eBay', 'Amazon']
                    else:
                        tortlist = tortlist + obj[0].strip().split(',')

            tortlist = set(tortlist)
            if len(tortlist) >= 1:
                tort = '|'.join(tortlist)
                self.set_tort_by_mainsku(mainsku, tort)
        if tort is not None:
            tort = tort.split('|')
        return tort

    # set 侵权状态  add by wangzy 20180525
    def set_tortstatus_by_mainsku(self, mainsku, status):
        return self.__private_set_attr(mainsku, 'TortInfo', status)

    # get 侵权状态  add by wangzy 20180525
    def get_tortstatus_by_mainsku(self, mainsku):
        tortInfo = self.__private_get_attr(mainsku, 'TortInfo')
        return tortInfo