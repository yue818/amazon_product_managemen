# -*- coding: utf-8 -*-
"""  
 @desc: 各平台算价表,总公式算价机制如下:(成本(￥)+运费(￥))/汇率/(1-利润率-平台扣点比率) = 最终售价(目标币种)
 @author: chenchen  
 @site: 
 @software: PyCharm
 @file: calculate_price.py
 @time: 2018/4/14 08:40
""" 


from skuapp.table.t_cfg_b_currencycode import *
from skuapp.table.t_cfg_b_emsfare2 import *
from skuapp.table.t_cfg_b_emsfare_country2 import *
from skuapp.table.t_cfg_b_logisticway import *
from skuapp.table.t_cfg_platform_country import *
from skuapp.table.t_cfg_bracket import *
from skuapp.table.t_cfg_b_country import *
from pyapp.models import b_goods as py_b_goods
from django.contrib import messages


class calculate_price():
    def __init__(self,SKU):
        self.SKU = SKU
        try:
            b_goods_obj = py_b_goods.objects.get(SKU=SKU)
            self.Money = str(b_goods_obj.CostPrice)
            self.Weight = str(b_goods_obj.Weight)
        except:
            self.Money = None
            self.Weight = None

    # 计算售价
    # Weight 商品原始克重(g)
    # Money  商品原始成本(人民币)
    # profitRate 利润率 默认0
    # 返回三种不同货币类型的售价,数据类型dic
    def calculate_selling_price(self,profitRate,platformCountryCode='JOOM-RUS', DestinationCountryCode='RUS',Money=None,Weight=None):
        try:
            Money = float(self.Money)
            Weight = float(self.Weight)
        except:
            Money = float(Money)
            Weight = float(Weight)
        profitRate = float(profitRate)

        error_info = {'error_code':200,'error_info':'信息获取成功!'}
        # 根据页面的目的地国家和平台国家编号去找物流方式编号
        t_cfg_b_emsfare2_obj = t_cfg_b_emsfare2.objects.get(platform_country_code=platformCountryCode, countrycode=DestinationCountryCode)
        logisticwaycode_expression = str(t_cfg_b_emsfare2_obj.logisticwaycode)
        logisticwaycode_desc = t_cfg_b_emsfare2_obj.logisticwaycode_desc
        scope = {'sell_price':0,'Weight':Weight}
        exec(logisticwaycode_expression,scope)
        logisticwaycode = scope['waycode']
        #根据当前平台国家编号获取当前货币编号以及平台扣点
        kickback = float(t_cfg_b_emsfare2_obj.kickback)
        CURRENCYCODE = None
        basefee = None
        try:
            t_cfg_platform_country_obj = t_cfg_platform_country.objects.get(platform_country_code=platformCountryCode)
            #kickback = float(t_cfg_platform_country_obj.kickback)
            basefee = float(t_cfg_platform_country_obj.basefee)
            t_cfg_b_country_obj = t_cfg_b_country.objects.get(country_code=DestinationCountryCode)
            CURRENCYCODE = t_cfg_b_country_obj.CURRENCYCODE
            ExchangeRate_basefee = t_cfg_b_currencycode.objects.get(CURRENCYCODE=CURRENCYCODE).ExchangeRate
            basefee = basefee * float(ExchangeRate_basefee)
        except:
            error_info = {'error_code': 2, 'error_info': '平台扣点/目的国家货币名称/ 当中没有配置！'}
            

        # 计算售价=成本价+运费
        if 1 - profitRate / 100 - kickback / 100 == 0:
            error_info = {'error_code': 7, 'error_info': '利润率和平台扣点有冲突！'}
            return

        #根据货币编号获取人民币汇率
        ExchangeRate = None
        try:
            t_cfg_b_currencycode_obj = t_cfg_b_currencycode.objects.get(CURRENCYCODE=CURRENCYCODE)
            ExchangeRate = float(t_cfg_b_currencycode_obj.ExchangeRate)
        except:
            error_info = {'error_code': 3, 'error_info': '当前货币与人民币汇率 没有配置！'}
            

        #获取美元与人民币汇率
        ExchangeRate_USD = None
        try:
            t_cfg_b_currencycode_obj = t_cfg_b_currencycode.objects.get(CURRENCYCODE='USD')
            ExchangeRate_USD = float(t_cfg_b_currencycode_obj.ExchangeRate)
        except:
            error_info = {'error_code': 4, 'error_info': '美元与人民币汇率 没有配置！'}
            

        #根据物流方式编号和目的国家编号去查询基本运费计算规则
        try:
            t_cfg_b_emsfare_country2_obj = t_cfg_b_emsfare_country2.objects.get(country_code=DestinationCountryCode,
                                                                              logisticwaycode=logisticwaycode)
            getprice_expression = str(t_cfg_b_emsfare_country2_obj.getprice)
            getprice_desc = t_cfg_b_emsfare_country2_obj.getprice_desc
            scope2 = {'Weight': Weight} 
            exec(getprice_expression, scope2)
            price_yf = scope2['Price']
            Bracketid = t_cfg_b_emsfare_country2_obj.Bracketid
        except:
            error_info = {'error_code': 5, 'error_info': '基础费用/初始价格/初始重量/增加价格/增加重量 没有配置！'}
            
        
        #根据一次算价的物流方式得到的外键Bracketid获取分档价格
        try:
            fd_money     = float(t_cfg_bracket.objects.filter(bracketid=Bracketid,weight__gte=Weight).order_by('weight').values_list('money',flat=True)[:1][0])
            CURRENCYCODE = t_cfg_bracket.objects.filter(bracketid=Bracketid,weight__gte=Weight).order_by('weight').values_list('CURRENCYCODE',flat=True)[:1][0]
            ExchangeRate2 = t_cfg_b_currencycode.objects.get(CURRENCYCODE=CURRENCYCODE).ExchangeRate
            fd_money     = fd_money * float(ExchangeRate2)
        except:
            fd_money = 0

        #一次算价,获取对应物流中文名称以及物流折扣
        logisticName = None
        Discount = None
        try:
            t_cfg_b_logisticway_obj = t_cfg_b_logisticway.objects.get(code=logisticwaycode)
            logisticName = t_cfg_b_logisticway_obj.name
            Discount = float(t_cfg_b_logisticway_obj.Discount)
        except:
            error_info = {'error_code': 6, 'error_info': '物流方式名称/物流折扣 没有配置！'}
            

        #一次算价得到最终售价
        sellingPrice_destination = ((price_yf+fd_money) * Discount/100 + Money + basefee)/ExchangeRate/(1-profitRate/100-kickback/100)   #目的国家售价
        sellingPrice_china = sellingPrice_destination*ExchangeRate
        sellingPrice_us = sellingPrice_destination*ExchangeRate/ExchangeRate_USD
        sellingPrice1 = round(sellingPrice_us, 2)
        params_flow1 = {'flag':01,'logisticwaycode_desc':logisticwaycode_desc,'getprice_desc':getprice_desc,'sellingPrice1':sellingPrice1,'price_yf':price_yf,'fd_money':fd_money,'Discount':Discount,'Money':Money,'basefee':basefee,'ExchangeRate_USD':ExchangeRate_USD,'profitRate':profitRate,'kickback':kickback,'logisticwaycode_expression':logisticwaycode_expression}
        #二次算价重新给域赋值
        scope3 = {'Weight': Weight,'sell_price': sellingPrice1}
        exec(logisticwaycode_expression, scope3)
        pricelimit_logisticwaycode = scope3['waycode']
        #二次算价,获取对应物流中文名称以及平台折扣
        try:
            t_cfg_b_logisticway_obj = t_cfg_b_logisticway.objects.get(code=pricelimit_logisticwaycode)
            logisticName = t_cfg_b_logisticway_obj.name
            Discount = float(t_cfg_b_logisticway_obj.Discount)
        except:
            logisticName = None
            Discount = None
        #二次算价获取运费
        t_cfg_b_emsfare_country2_obj = t_cfg_b_emsfare_country2.objects.get(country_code=DestinationCountryCode, logisticwaycode=pricelimit_logisticwaycode)
        getprice_expression = t_cfg_b_emsfare_country2_obj.getprice
        getprice_desc = t_cfg_b_emsfare_country2_obj.getprice_desc
        scope4 = {'Weight': Weight} 
        exec(getprice_expression,scope4)
        price_yf = scope4['Price']
        Bracketid = t_cfg_b_emsfare_country2_obj.Bracketid
        #二次算价获取分档运费
        try:
            fd_money     = float(t_cfg_bracket.objects.filter(bracketid=Bracketid, weight__gte=Weight).order_by('weight').values_list('money', flat=True)[:1][0])
            CURRENCYCODE = t_cfg_bracket.objects.filter(bracketid=Bracketid,weight__gte=Weight).order_by('weight').values_list('CURRENCYCODE',flat=True)[:1][0]
            ExchangeRate2 = t_cfg_b_currencycode.objects.get(CURRENCYCODE=CURRENCYCODE).ExchangeRate
            fd_money     = fd_money * float(ExchangeRate2)
        except:
            fd_money = 0

        sellingPrice_destination = ((price_yf+fd_money) * Discount / 100 + Money + basefee) / ExchangeRate / (1 - profitRate / 100 - kickback / 100)  # 目的国家售价
        sellingPrice_china = sellingPrice_destination * ExchangeRate
        sellingPrice_us = sellingPrice_destination * ExchangeRate / ExchangeRate_USD
        sellingPrice2 = round(sellingPrice_us, 2)
        params_flow2 = {'flag':02,'logisticwaycode_desc':logisticwaycode_desc,'getprice_desc':getprice_desc,'price_yf':price_yf,'fd_money':fd_money,'Discount':Discount,'Money':Money,'basefee':basefee,'ExchangeRate_USD':ExchangeRate_USD,'profitRate':profitRate,'kickback':kickback,'logisticwaycode_expression':logisticwaycode_expression}
        
        #保留俩位小数点
        sellingPrice_destination = round(sellingPrice_destination, 2)
        sellingPrice_china = round(sellingPrice_china, 2)
        sellingPrice_us = round(sellingPrice_us, 2)
        
        #sellingPrice 最终售价,同时获取 logisticName物流方式,kickback平台扣点,ExchangeRate汇率,Discount物流折扣 以dic形式返回=>
        if sellingPrice1 == sellingPrice2:
            params = {'sellingPrice_destination':sellingPrice_destination,'sellingPrice_china':sellingPrice_china,'sellingPrice_us':sellingPrice_us,'logisticName':logisticName,'CURRENCYCODE':CURRENCYCODE,'kickback':kickback,'ExchangeRate':ExchangeRate,'Discount':Discount,'params_flow':params_flow1}
        else:
            params = {'sellingPrice_destination':sellingPrice_destination,'sellingPrice_china':sellingPrice_china,'sellingPrice_us':sellingPrice_us,'logisticName':logisticName,'CURRENCYCODE':CURRENCYCODE,'kickback':kickback,'ExchangeRate':ExchangeRate,'Discount':Discount,'params_flow':params_flow2,'params_flow1':params_flow1}
        return params

    # 计算利润率
    # platformCountryCode=t_cfg_b_emsfare.platform_country_code
    # Weight 商品原始克重(g)
    # Money  商品原始成本(人民币)
    # sellingPrice 售价(人民币，显示的是加入汇率计算)
    # 返回profitRate利润率(百分制,15就是 15%)
    #(成本(￥)+运费(￥))/汇率/(1-利润率-平台扣点比率) = 最终售价(目标币种)
    def calculate_profitRate(self, sellingPrice,platformCountryCode='JOOM-RUS', DestinationCountryCode='RUS',Money=None,Weight=None):
        try:
            Money = float(self.Money)
            Weight = float(self.Weight)
        except:
            Money = float(Money)
            Weight = float(Weight)
        try:
            sellingPrice = float(sellingPrice)
        except:
            sellingPrice = -1
        #获取美元与人民币汇率
        try:
            t_cfg_b_currencycode_obj = t_cfg_b_currencycode.objects.get(CURRENCYCODE='USD')
            ExchangeRate_USD = float(t_cfg_b_currencycode_obj.ExchangeRate)
        except:
            ExchangeRate_USD = None
        #根据当前平台国家编号获取当前货币编号以及平台扣点
        try:
            t_cfg_platform_country_obj = t_cfg_platform_country.objects.get(platform_country_code=platformCountryCode)
            t_cfg_b_emsfare2_obj = t_cfg_b_emsfare2.objects.get(platform_country_code=platformCountryCode, countrycode=DestinationCountryCode)
            kickback = float(t_cfg_b_emsfare2_obj.kickback)
            t_cfg_b_country_obj = t_cfg_b_country.objects.get(country_code=DestinationCountryCode)
            basefee = float(t_cfg_platform_country_obj.basefee)
            CURRENCYCODE = t_cfg_b_country_obj.CURRENCYCODE
            ExchangeRate_basefee = t_cfg_b_currencycode.objects.get(CURRENCYCODE=CURRENCYCODE).ExchangeRate
            basefee = basefee * float(ExchangeRate_basefee)
        except:
            kickback = None
            CURRENCYCODE = None
            basefee = None
        #根据货币编号获取人民币汇率
        try:
            t_cfg_b_currencycode_obj = t_cfg_b_currencycode.objects.get(CURRENCYCODE=CURRENCYCODE)
            ExchangeRate = float(t_cfg_b_currencycode_obj.ExchangeRate)
        except:
            ExchangeRate = None
       # 根据页面的目的地国家和平台国家编号去找默认物流方式编号，最大价格限制以及超过最大价格后采取的新的物流方式编号
        t_cfg_b_emsfare2_obj = t_cfg_b_emsfare2.objects.get(platform_country_code=platformCountryCode, countrycode=DestinationCountryCode)
        logisticwaycode_expression = str(t_cfg_b_emsfare2_obj.logisticwaycode)
        scope = {'sell_price':sellingPrice,'Weight':Weight}
        exec(logisticwaycode_expression,scope)
        waycode = scope['waycode']
                
        try:
            t_cfg_b_logisticway_obj = t_cfg_b_logisticway.objects.get(code=waycode)
            logisticName = t_cfg_b_logisticway_obj.name
            Discount = float(t_cfg_b_logisticway_obj.Discount)
        except:
            logisticName = None
            Discount = None
        # 根据物流方式编号和目的国家编号去查询基本运费计算规则
        t_cfg_b_emsfare_country2_obj = t_cfg_b_emsfare_country2.objects.get(country_code=DestinationCountryCode, logisticwaycode=waycode)
        getprice_expression = t_cfg_b_emsfare_country2_obj.getprice
        scope2 = {'Weight': Weight} 
        exec(getprice_expression,scope2)
        price_yf = scope2['Price']
        Bracketid = t_cfg_b_emsfare_country2_obj.Bracketid
        #二次算价获取分档运费
        try:
            fd_money     = float(t_cfg_bracket.objects.filter(bracketid=Bracketid, weight__gte=Weight).order_by('weight').values_list('money', flat=True)[:1][0])
            CURRENCYCODE = float(t_cfg_bracket.objects.filter(bracketid=Bracketid,weight__gte=Weight).order_by('weight').values_list('CURRENCYCODE',flat=True)[:1][0])
            ExchangeRate = t_cfg_b_currencycode.objects.get(CURRENCYCODE=CURRENCYCODE).ExchangeRate
            fd_money     = fd_money * float(ExchangeRate)
        except:
            fd_money = 0
        sum_money = (price_yf + fd_money) * Discount / 100.0 + Money + basefee
        #计算利润率
        profitRate = (1- kickback/100 - sum_money/ExchangeRate_USD/sellingPrice)*10.0*10.0
        if sellingPrice == -1:
            profitRate = 99999
        profitRate = round(profitRate, 2)
        #获取人民币以及目标国家货币价值
        sellingPrice_china = sellingPrice * ExchangeRate_USD
        sellingPrice_destination = sellingPrice_china / ExchangeRate
        params = {'price_yf':price_yf,'fd_money':fd_money,'basefee':basefee,'sellingPrice_destination': sellingPrice_destination, 'sellingPrice_china': sellingPrice_china,
                  'logisticName': logisticName, 'CURRENCYCODE': CURRENCYCODE,'ExchangeRate_USD':ExchangeRate_USD,'Discount':Discount,'Money':Money,'sum_money':sum_money,'sellingPrice':sellingPrice,
                  'kickback': kickback, 'ExchangeRate': ExchangeRate, 'Discount': Discount,'profitRate':profitRate}
        return params
