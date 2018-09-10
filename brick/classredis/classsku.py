# -*- coding: utf-8 -*-
"""  
 @desc:  
 @author: 李杨杨  
 @site: 
 @software: PyCharm
 @file: classsku.py
 @time: 2017-12-27 13:14

"""
import re
from django.db import connection
from django_redis import get_redis_connection
connRedis = get_redis_connection(alias='product')

class classsku():
    def __init__(self,db_cnxn=connection,redis_cnxn=connRedis):
        self.db_cnxn = db_cnxn
        self.redis_cnxn = redis_cnxn

    def __private_set_attr(self,name,key,value):
        if self.redis_cnxn is not None and value is not None:
            self.redis_cnxn.hset(name, key,value)

    def __private_get_attr(self,name,key):
        if self.redis_cnxn is not None:
            return self.redis_cnxn.hget(name,key)

    # 子SKU 状态
    def set_goodsstatus_by_sku(self,sku,status):
        self.__private_set_attr(sku,'GoodsStatus',status)
    def get_goodsstatus_by_sku(self,sku):
        goodsstatus = self.__private_get_attr(sku,'GoodsStatus')
        if goodsstatus is None and self.db_cnxn is not None:
            stacur = self.db_cnxn.cursor()
            stacur.execute('select GoodsStatus,used from py_db.b_goods WHERE SKU = %s ;',(sku,))
            obj = stacur.fetchone()
            if obj:
                used = obj[1]
                goodsstatus = obj[0]
                if int(used) == 1:
                    goodsstatus = '4' # 停售
                else:
                    stacur.execute('select statuscode from goodsstatus_compare WHERE hq_GoodsStatus = %s ;', (goodsstatus,))
                    obj = stacur.fetchone()
                    if obj:
                        goodsstatus = obj[0]
                self.set_goodsstatus_by_sku(sku,goodsstatus)
            stacur.close()
        if goodsstatus == '1' or goodsstatus == u'1-正常':
            goodsstatus = u'正常'
        if goodsstatus == '2' or goodsstatus == u'2-售完下架':
            goodsstatus = u'售完下架'
        if goodsstatus == '3' or goodsstatus == u'3-临时下架':
            goodsstatus = u'临时下架'
        if goodsstatus == '4' or goodsstatus == u'4-停售':
            goodsstatus = u'停售'
        return goodsstatus

    # 子SKU 价格
    def set_price_by_sku(self,sku,price):
        self.__private_set_attr(sku,'CostPrice',price)
    def get_price_by_sku(self,sku):
        price = self.__private_get_attr(sku,'CostPrice')
        if price is None and self.db_cnxn is not None:
            pricur = self.db_cnxn.cursor()
            pricur.execute('select UnitPrice from t_product_mainsku_sku WHERE ProductSKU = %s ;',(sku,))
            obj = pricur.fetchone()
            if obj:
                price = obj[0]
            if not price:
                pricur.execute('select CostPrice from py_db.b_goods WHERE SKU = %s ;', (sku,))
                obj = pricur.fetchone()
                if obj:
                    price = obj[0]
            if price is not None:
                self.set_price_by_sku(sku,price)
            pricur.close()
        return price

    # 子SKU 重量
    def set_weight_by_sku(self,sku,weight):
        self.__private_set_attr(sku,'Weight',weight)
    def get_weight_by_sku(self,sku):
        weight = self.__private_get_attr(sku,'Weight')
        if weight is None and self.db_cnxn is not None:
            weicur = self.db_cnxn.cursor()
            weicur.execute('select Weight from t_product_mainsku_sku WHERE ProductSKU = %s ;',(sku,))
            obj = weicur.fetchone()
            if obj:
                weight = obj[0]
            if not weight:
                weicur.execute('select Weight from py_db.b_goods WHERE SKU = %s ;', (sku,))
                obj = weicur.fetchone()
                if obj:
                    weight = obj[0]
            if weight is not None:
                self.set_weight_by_sku(sku,weight)
            weicur.close()
        return weight

    # 子SKU 包装规格
    def set_packinfo_by_sku(self,sku,packinfo):
        self.__private_set_attr(sku,'PackInfo',packinfo)
    def get_packinfo_by_sku(self,sku):
        packinfo = self.__private_get_attr(sku,'PackInfo')
        if packinfo is None and self.db_cnxn is not None:
            paccur = self.db_cnxn.cursor()
            paccur.execute('select PackNID from t_product_mainsku_sku WHERE ProductSKU = %s ;',(sku,))
            obj = paccur.fetchone()
            if obj:
                packnid = obj[0]
                paccur.execute('select PackName from py_db.b_packinfo WHERE NID = %s ;', (packnid,))
                packobj = paccur.fetchone()
                if packobj:
                    packinfo = packobj[0]
                    self.set_packinfo_by_sku(sku,packinfo)
        return packinfo

    # 子SKU所属 主SKU
    def set_bemainsku_by_sku(self,sku,bemainsku):
        self.__private_set_attr(sku,'MainSKU',bemainsku)
    def get_bemainsku_by_sku(self,sku):
        bemainsku = self.__private_get_attr(sku,'MainSKU')
        if bemainsku is None and self.db_cnxn is not None:
            becur = self.db_cnxn.cursor()
            becur.execute('select MainSKU from t_product_mainsku_sku WHERE ProductSKU = %s ;', (sku,))
            obj = becur.fetchone()
            if obj:
                bemainsku = obj[0]
            if sku and bemainsku is None:
                slist = re.findall(r'[0-9]+|[a-z-]+|[A-Z-|]+', sku)
                if len(slist) >= 2:
                    bemainsku = '%s%s' % (slist[0], slist[1])
                else:
                    bemainsku = ''.join(slist)
            if bemainsku:
                self.set_bemainsku_by_sku(sku, bemainsku)
        return bemainsku

    # 子SKU绑定的 ShopSKU
    def set_shopsku_by_sku(self,sku,shopsku):
        self.__private_set_attr(sku,'ShopSKU',shopsku)
    def get_shopsku_by_sku(self,sku):
        shopsku = self.__private_get_attr(sku,'ShopSKU')
        if shopsku is None and self.db_cnxn is not None:
            shopcur = self.db_cnxn.cursor()
            shopcur.execute('select ShopSKU from py_db.b_goodsskulinkshop WHERE SKU = %s ;',(sku,))
            objs = shopcur.fetchall()
            shopcur.close()
            shopskulist = []
            for obj in objs:
                if obj and obj[0] is not None:
                    shopskulist.append(obj[0])
            if len(shopskulist) >= 1:
                shopsku = '|'.join(shopskulist)
                self.set_shopsku_by_sku(sku,shopsku)
        if shopsku is not None:
            shopsku = shopsku.split('|')
        return shopsku

    # 商品SKU 采购未入库量
    def set_uninstore_by_sku(self, sku, value):
        self.__private_set_attr(sku, 'NotInStore', value)
    def get_uninstore_by_sku(self, sku):
        return self.__private_get_attr(sku, 'NotInStore')

    # 商品SKU 库存量
    def set_number_by_sku(self, sku, value):
        self.__private_set_attr(sku, 'Number', value)
    def get_number_by_sku(self, sku):
        return self.__private_get_attr(sku, 'Number')

    # 商品SKU 库存占用量
    def set_reservationnum_by_sku(self, sku, value):
        self.__private_set_attr(sku, 'ReservationNum', value)
    def get_reservationnum_by_sku(self, sku):
        return self.__private_get_attr(sku, 'ReservationNum')

    # 商品SKU 可卖天数
    def set_cansaleday_by_sku(self, sku, value):
        self.__private_set_attr(sku, 'CanSaleDay', value)
    def get_cansaleday_by_sku(self, sku):
        return self.__private_get_attr(sku, 'CanSaleDay')

    # 商品SKU 7天销量
    def set_sellcount1_by_sku(self, sku, value):
        self.__private_set_attr(sku, 'SellCount1', value)
    def get_sellcount1_by_sku(self, sku):
        return self.__private_get_attr(sku, 'SellCount1')

    # 商品SKU 商品预计可用库存
    def set_hopeusenum_by_sku(self, sku, value):
        self.__private_set_attr(sku, 'HopeUseNum', value)
    def get_hopeusenum_by_sku(self, sku):
        return self.__private_get_attr(sku, 'HopeUseNum')

    # 商品SKU 商品缺货及未派单数量
    def set_unpaidnum_by_sku(self, sku, value):
        self.__private_set_attr(sku, 'UnPaiDNum', value)
    def get_unpaidnum_by_sku(self, sku):
        return self.__private_get_attr(sku, 'UnPaiDNum')

    # 商品SKU 库位
    def set_location_by_sku(self, sku, value):
        self.__private_set_attr(sku, 'Location', value)
    def get_location_by_sku(self, sku):
        return self.__private_get_attr(sku, 'Location')

    # 店铺SKU  7天销量
    def set_shopsevensale_by_sku(self, shopsku, value):
        self.__private_set_attr(shopsku, 'SevenSales', value)
    def get_shopsevensale_by_sku(self, shopsku):
        return self.__private_get_attr(shopsku, 'SevenSales')

    # 商品SKU 设置更新时间
    def set_updatetime_by_sku(self, sku, value):
        self.__private_set_attr(sku, 'UpdateTime', value)
    def get_updatetime_by_sku(self, sku):
        return self.__private_get_attr(sku, 'UpdateTime')

    # 商品SKU 是否带电
    def set_isCharged_by_sku(self, sku, value):
        self.__private_set_attr(sku, 'isCharged', value)

    def get_isCharged_by_sku(self, sku):
        return self.__private_get_attr(sku, 'isCharged')

    #单商品SKU 获取属性值 返回字典
    def get_skuallattrvalue_by_sku(self, sku):
        DicResult = {}
        DicResult["GoodsStatus"] = self.get_goodsstatus_by_sku(sku) #商品状态
        DicResult["CostPrice"] = self.get_price_by_sku(sku) #商品价格
        DicResult["Weight"] = self.get_weight_by_sku(sku) #商品重量
        DicResult["PackInfo"] = self.get_packinfo_by_sku(sku) #商品包装信息
        DicResult["MainSKU"] = self.get_bemainsku_by_sku(sku) #商品主SKU
        DicResult["ShopSKU"] = self.get_shopsku_by_sku(sku) #商品店铺SKU
        DicResult["NotInStore"] = self.get_uninstore_by_sku(sku) #浦江采购未入库
        DicResult["Number"] = self.get_number_by_sku(sku) #商品库存量
        DicResult["ReservationNum"] = self.get_reservationnum_by_sku(sku) #商品占用量
        DicResult["CanSaleDay"] = self.get_cansaleday_by_sku(sku) #商品可卖天数
        DicResult["SellCount1"] = self.get_sellcount1_by_sku(sku) #商品7天销量
        DicResult["HopeUseNum"] = self.get_hopeusenum_by_sku(sku)  # 商品7天销量
        DicResult["UnPaiDNum"] = self.get_unpaidnum_by_sku(sku)  # 商品7天销量
        DicResult["Location"] = self.get_location_by_sku(sku)  # 商品7天销量
        DicResult["ShopSKU"] = self.get_shopsevensale_by_sku(sku)  # 店铺SKU  7天销量
        DicResult["UpdateTime"] = self.get_updatetime_by_sku(sku) #商品属性redis刷新时间
        return DicResult

    # 多个商品SKU 获取属性值  参数skuList 列表  返回字典
    def get_multiskuallattrvalue_by_sku(self, skuList):
        DicResult = {}
        for row in skuList:
            dicTmp = self.get_skuallattrvalue_by_sku(row)
            DicResult[row] = dicTmp
        return DicResult

    # 多个商品SKU 多个属性设置、获取{sku:{attr1:value,attr2:value,attr3:value},sku1:{attr1:value,attr2:value,attr3:value}}
    def set_multisku_multiattr_by_sku(self, DicMultiSKU_Attr):
        if self.redis_cnxn is not None:
            try:
                with self.redis_cnxn.pipeline(transaction=False) as p:
                    for keySKU in DicMultiSKU_Attr.keys():
                        skuAttr = DicMultiSKU_Attr[keySKU]
                        for keyAttr in skuAttr.keys():
                            value = skuAttr[keyAttr]
                            p.hset(keySKU,keyAttr,value)
                    p.execute()
            except Exception as e:
                return 10002
        else:
            return 10001
        return 10000
    #获取结果：入参：{sku:[attr1,attr2],sku1:[attr1,attr2]}
    # 返回：{sku:{attr1:value,attr2:value},sku1:{attr1:value,attr2:value}}
    def get_multisku_multiattr_by_sku(self, DicMultiSKU_Attr):
        resultDic = {}
        sResult = []
        if self.redis_cnxn is not None:
            try:
                with self.redis_cnxn.pipeline(transaction=False) as p:
                    for keySKU in sorted(DicMultiSKU_Attr.keys()):
                        skuAttr = DicMultiSKU_Attr[keySKU]
                        for keyAttr in skuAttr:
                            p.hget(keySKU,keyAttr)
                    sResult = p.execute()
                i = 0
                for keySKU in sorted(DicMultiSKU_Attr.keys()):
                    skuAttr = DicMultiSKU_Attr[keySKU]
                    dicTmp = {}
                    for keyAttr in skuAttr:
                        dicTmp[keyAttr] = sResult[i]
                        i += 1
                    resultDic[keySKU] = dicTmp
            except Exception as e:
                return 10002
        else:
            return 10001
        return resultDic

#classsku_obj = classsku(connection,connRedis)
# classsku_obj.set_uninstore_by_sku('test0001',20)
# print classsku_obj.get_skuallattrvalue_by_sku("test0002")
# print classsku_obj.get_multiskuallattrvalue_by_sku(['test0002','test0003'])
# classsku_obj.set_multisku_multiattr_by_sku({'test0002':{'19':30,'Number':50},'test0003':{'Price':30.0,'CanSaleDay':50}})
# print classsku_obj.get_multisku_multiattr_by_sku({'test0002':['19','Number'],'test0003':['Price','CanSaleDay'],'test0001':['CanSaleDay']})
# print classsku_obj.get_skuallattrvalue_by_sku(u"新款自拍王白色")



