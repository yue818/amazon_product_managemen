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
from skuapp.table.t_cfg_b_emsfare import *
from skuapp.table.t_cfg_b_emsfare_country import *
from skuapp.table.t_cfg_b_logisticway import *
from skuapp.table.t_cfg_platform_country import *
from skuapp.table.t_cfg_bracket import *
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
    # platformCountryCode=t_cfg_b_emsfare.platform_country_code
    # Weight 商品原始克重(g)
    # Money  商品原始成本(人民币)
    # profitRate 利润率 默认0
    # 返回sellingPrice售价(人民币，显示的是加入汇率计算)
    def calculate_selling_price(self,profitRate,platformCountryCode='JOOM-RUS', DestinationCountryCode='RUS',Money=None,Weight=None):
        try:
            Money = float(self.Money)
            Weight = float(self.Weight)
        except:
            Money = float(Money)
            Weight = float(Weight)
        profitRate = float(profitRate)

        error_info = {'error_code':200,'error_info':'信息获取成功!'}
        # 根据页面的目的地国家和平台国家编号去找[[seq为0已去掉]]的默认物流方式编号，最大价格限制以及超过最大价格后采取的新的物流方式编号
        logisticwaycode = None
        weightlimit = None
        weightlimit_logisticwaycode = None
        pricelimit = None
        pricelimit_logisticwaycode = None
        weightlimit2 = None
        weightlimit2_logisticwaycode = None
        try:
            t_cfg_b_emsfare_obj = t_cfg_b_emsfare.objects.get(platform_country_code=platformCountryCode,
                                                              countrycode=DestinationCountryCode)
            logisticwaycode = t_cfg_b_emsfare_obj.logisticwaycode
            weightlimit = float(t_cfg_b_emsfare_obj.weightlimit)
            weightlimit_logisticwaycode = t_cfg_b_emsfare_obj.weightlimit_logisticwaycode
            weightlimit2 = float(t_cfg_b_emsfare_obj.weightlimit2)
            weightlimit2_logisticwaycode = t_cfg_b_emsfare_obj.weightlimit2_logisticwaycode
            pricelimit = float(t_cfg_b_emsfare_obj.pricelimit)
            pricelimit_logisticwaycode = t_cfg_b_emsfare_obj.pricelimit_logisticwaycode
        except:
            error_info = {'error_code':1,'error_info':'物流方式编号/最大价格限制/超出最大价格限制的物流方式编号 当中没有配置！'}
            

        if weightlimit == 0 and weightlimit2 == 0:
            logisticwaycode = logisticwaycode
        elif weightlimit != 0 and weightlimit2 == 0:
            if Weight <= weightlimit:
                logisticwaycode = logisticwaycode
            else:
                logisticwaycode = weightlimit_logisticwaycode
        elif weightlimit != 0 and weightlimit2 != 0:
            if Weight <= weightlimit:
                logisticwaycode = logisticwaycode
            elif Weight > weightlimit and Weight <= weightlimit2:
                logisticwaycode = weightlimit_logisticwaycode 
            else:
                logisticwaycode = weightlimit2_logisticwaycode
        #根据当前平台国家编号获取当前货币编号以及平台扣点
        kickback = None
        CURRENCYCODE = None
        try:
            t_cfg_platform_country_obj = t_cfg_platform_country.objects.get(platform_country_code=platformCountryCode)
            kickback = float(t_cfg_platform_country_obj.kickback)
            CURRENCYCODE = t_cfg_platform_country_obj.CURRENCYCODE
        except:
            error_info = {'error_code': 2, 'error_info': '平台扣点/目的国家货币名称/ 当中没有配置！'}
            

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
            

        # 根据默认的物流方式编号和目的国家编号去查询基本运费计算规则
        BaseMoney = None
        BeginWeight = None
        BeginMoney = None
        AddWeight = None
        AddMoney = None
        Bracketid = None
            
        
        try:
            t_cfg_b_emsfare_country_obj = t_cfg_b_emsfare_country.objects.get(country_code=DestinationCountryCode,
                                                                              logisticwaycode=logisticwaycode)
            BaseMoney = float(t_cfg_b_emsfare_country_obj.BaseMoney)
            BaseMoney1 = BaseMoney
            BeginWeight = float(t_cfg_b_emsfare_country_obj.BeginWeight)
            BeginWeight1 = BeginWeight
            BeginMoney = float(t_cfg_b_emsfare_country_obj.BeginMoney)
            BeginMoney1 = BeginMoney
            AddWeight = float(t_cfg_b_emsfare_country_obj.AddWeight)
            AddWeight1 = AddWeight
            AddMoney = float(t_cfg_b_emsfare_country_obj.AddMoney)
            AddMoney1 = AddMoney
            Bracketid = int(t_cfg_b_emsfare_country_obj.Bracketid)
        except:
            error_info = {'error_code': 5, 'error_info': '基础费用/初始价格/初始重量/增加价格/增加重量 没有配置！'}
            
        
        #获取分档价格
        try:
            fd_money = float(t_cfg_bracket.objects.filter(bracketid=Bracketid,weight__gte=Weight).order_by('weight').values_list('money',flat=True)[:1][0])
        except:
            fd_money = 0

        # 一次算价,获取对应物流中文名称以及物流折扣
        logisticName = None
        Discount = None
        try:
            t_cfg_b_logisticway_obj = t_cfg_b_logisticway.objects.get(code=logisticwaycode)
            logisticName = t_cfg_b_logisticway_obj.name
            Discount = float(t_cfg_b_logisticway_obj.Discount)
            Discount1 = Discount
        except:
            error_info = {'error_code': 6, 'error_info': '物流方式名称/物流折扣 没有配置！'}
            

        # 计算售价=成本价+运费
        if 1 - profitRate / 100 - kickback / 100 == 0:
            error_info = {'error_code': 7, 'error_info': '利润率和平台扣点有冲突！'}
            
        if Weight <= BeginWeight:
            sellingPrice_destination = ((BaseMoney1+BeginMoney1)*Discount/100 + Money + fd_money)/ExchangeRate/(1-profitRate/100-kickback/100)   #目的国家售价
            sellingPrice_china = sellingPrice_destination*ExchangeRate
            sellingPrice_us = sellingPrice_destination*ExchangeRate/ExchangeRate_USD
            sellingPrice = round(sellingPrice_us, 2)
            params_flow = {'flag':01,'BaseMoney':BaseMoney,'BeginMoney':BeginMoney,'Discount':Discount,'sellingPrice':sellingPrice,'Money':Money,'ExchangeRate':ExchangeRate,'ExchangeRate_USD':ExchangeRate_USD,'profitRate':profitRate,'kickback':kickback}
        else:
            extra_Weight = Weight - BeginWeight
            extra_Weight1 = extra_Weight
            if AddWeight is None or AddWeight == '':
                print 'AddWeight is None error!'
            else:
                sellingPrice = ((BaseMoney+BeginMoney + extra_Weight * AddMoney / AddWeight)*Discount/100+Money + fd_money)/ExchangeRate_USD/(1-profitRate/100-kickback/100)   #美元售价
                sellingPrice1 = round(sellingPrice, 2)
                # 一次算价
                if sellingPrice1 < pricelimit or pricelimit == 0:
                    #折换成目的地国家货币
                    sellingPrice_destination = sellingPrice*ExchangeRate_USD/ExchangeRate
                    sellingPrice_us = sellingPrice
                    sellingPrice_china = sellingPrice*ExchangeRate_USD
                    params_flow = {'flag':02,'BaseMoney':BaseMoney,'BeginMoney':BeginMoney,'extra_Weight':extra_Weight,'AddMoney':AddMoney,'AddWeight':AddWeight,'Discount':Discount,'sellingPrice':sellingPrice,'Money':Money,'ExchangeRate_USD':ExchangeRate_USD,'ExchangeRate':ExchangeRate,'profitRate':profitRate,'kickback':kickback}
                elif sellingPrice1 >= pricelimit and pricelimit != 0:
                    # 二次算价,获取对应物流中文名称以及平台折扣
                    try:
                        t_cfg_b_logisticway_obj = t_cfg_b_logisticway.objects.get(code=pricelimit_logisticwaycode)
                        logisticName = t_cfg_b_logisticway_obj.name
                        Discount = float(t_cfg_b_logisticway_obj.Discount)
                    except:
                        logisticName = None
                        Discount = None
                    # 二次算价
                    t_cfg_b_emsfare_country_obj = t_cfg_b_emsfare_country.objects.get(
                        country_code=DestinationCountryCode, logisticwaycode=pricelimit_logisticwaycode)
                    BaseMoney = float(t_cfg_b_emsfare_country_obj.BaseMoney)
                    BeginWeight = float(t_cfg_b_emsfare_country_obj.BeginWeight)
                    BeginMoney = float(t_cfg_b_emsfare_country_obj.BeginMoney)
                    AddWeight = float(t_cfg_b_emsfare_country_obj.AddWeight)
                    AddMoney = float(t_cfg_b_emsfare_country_obj.AddMoney)
                    if Weight <= BeginWeight:
                        sellingPrice_destination = ((BaseMoney+BeginMoney)*Discount/100 + Money + fd_money)/ExchangeRate/(1-profitRate/100-kickback/100)
                        sellingPrice_china = sellingPrice_destination * ExchangeRate
                        sellingPrice_us = sellingPrice_destination * ExchangeRate / ExchangeRate_USD
                        params_flow = {'flag': 11,'BaseMoney': BaseMoney,'BaseMoney1': BaseMoney1,'BeginMoney': BeginMoney,'BeginMoney1': BeginMoney1,'Discount':Discount,'Discount1':Discount1,'sellingPrice1':sellingPrice1,'Money':Money,'ExchangeRate':ExchangeRate,'ExchangeRate_USD':ExchangeRate_USD,'profitRate':profitRate,'kickback':kickback}
                    else:
                        extra_Weight = Weight - BeginWeight
                    if AddWeight is None or AddWeight == '':
                        messages.error(self.reuqest, 'AddWeight is None error!')
                    else:
                        sellingPrice_destination = ((BaseMoney+BeginMoney + extra_Weight * AddMoney / AddWeight)*Discount/100+Money + fd_money)/ExchangeRate/(1-profitRate/100-kickback/100)     #目的国家售价
                        sellingPrice_china = sellingPrice_destination*ExchangeRate
                        sellingPrice_us = sellingPrice_china/ExchangeRate_USD
                        params_flow = {'flag': 12, 'BaseMoney': BaseMoney,'BaseMoney1': BaseMoney1,'BeginMoney': BeginMoney,'BeginMoney1': BeginMoney1,'extra_Weight': extra_Weight,'extra_Weight1': extra_Weight1,'AddMoney': AddMoney,'AddMoney1': AddMoney1,'AddWeight': AddWeight,'AddWeight1': AddWeight1,'Discount':Discount,'Discount1':Discount1,'sellingPrice1':sellingPrice1,'Money':Money,'ExchangeRate_USD':ExchangeRate_USD,'ExchangeRate':ExchangeRate,'profitRate':profitRate,'kickback':kickback}

        sellingPrice_destination = round(sellingPrice_destination, 2)
        sellingPrice_china = round(sellingPrice_china, 2)
        sellingPrice_us = round(sellingPrice_us, 2)
        #sellingPrice 最终售价,同时获取 logisticName物流方式,kickback平台扣点,ExchangeRate汇率,Discount物流折扣 以dic形式返回=>
        params = {'sellingPrice_destination':sellingPrice_destination,'sellingPrice_china':sellingPrice_china,'sellingPrice_us':sellingPrice_us,'logisticName':logisticName,'CURRENCYCODE':CURRENCYCODE,'kickback':kickback,'ExchangeRate':ExchangeRate,'Discount':Discount,'params_flow':params_flow,'error_info':error_info}
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
        sellingPrice = float(sellingPrice)
        #获取美元与人民币汇率
        try:
            t_cfg_b_currencycode_obj = t_cfg_b_currencycode.objects.get(CURRENCYCODE='USD')
            ExchangeRate_USD = float(t_cfg_b_currencycode_obj.ExchangeRate)
        except:
            ExchangeRate_USD = None
        #根据当前平台国家编号获取当前货币编号以及平台扣点
        try:
            t_cfg_platform_country_obj = t_cfg_platform_country.objects.get(platform_country_code=platformCountryCode)
            kickback = float(t_cfg_platform_country_obj.kickback)
            CURRENCYCODE = t_cfg_platform_country_obj.CURRENCYCODE
        except:
            kickback = None
            CURRENCYCODE = None
        #根据货币编号获取人民币汇率
        try:
            t_cfg_b_currencycode_obj = t_cfg_b_currencycode.objects.get(CURRENCYCODE=CURRENCYCODE)
            ExchangeRate = float(t_cfg_b_currencycode_obj.ExchangeRate)
        except:
            ExchangeRate = None
        # 根据页面的目的地国家和平台国家编号去找默认物流方式编号，最大价格限制以及超过最大价格后采取的新的物流方式编号
        try:
            t_cfg_b_emsfare_obj = t_cfg_b_emsfare.objects.get(platform_country_code=platformCountryCode,
                                                              countrycode=DestinationCountryCode)
            logisticwaycode = t_cfg_b_emsfare_obj.logisticwaycode
            weightlimit = float(t_cfg_b_emsfare_obj.weightlimit)
            weightlimit_logisticwaycode = t_cfg_b_emsfare_obj.weightlimit_logisticwaycode
            weightlimit2 = float(t_cfg_b_emsfare_obj.weightlimit)
            weightlimit2_logisticwaycode = t_cfg_b_emsfare_obj.weightlimit_logisticwaycode
            pricelimit = float(t_cfg_b_emsfare_obj.pricelimit)
            pricelimit_logisticwaycode = t_cfg_b_emsfare_obj.pricelimit_logisticwaycode
        except:
            logisticwaycode = None
            pricelimit = None
            pricelimit_logisticwaycode = None
            weightlimit = None
            weightlimit_logisticwaycode = None
            weightlimit2 = None
            weightlimit2_logisticwaycode = None

        #获取对应物流中文名称以及物流折扣
        if pricelimit != 0:
            if sellingPrice < pricelimit:
                if weightlimit == 0 and weightlimit2 == 0:
                    waycode = logisticwaycode
                elif weightlimit != 0 and weightlimit2 == 0:
                    if Weight < weightlimit:
                        waycode = logisticwaycode
                    else:
                        waycode = weightlimit_logisticwaycode
                elif weightlimit != 0 and weightlimit2 != 0:
                    if Weight < weightlimit:
                        waycode = logisticwaycode
                    elif Weight >= weightlimit and Weight < weightlimit2:
                        waycode = weightlimit_logisticwaycode 
                    else:
                        waycode = weightlimit2_logisticwaycode
            else:
                waycode = pricelimit_logisticwaycode
        else:
            if weightlimit == 0:
                waycode = logisticwaycode
            else:
                if Weight <= weightlimit:
                    waycode = logisticwaycode
                else:
                    waycode = weightlimit_logisticwaycode
        try:
            t_cfg_b_logisticway_obj = t_cfg_b_logisticway.objects.get(code=waycode)
            logisticName = t_cfg_b_logisticway_obj.name
            Discount = float(t_cfg_b_logisticway_obj.Discount)
        except:
            logisticName = None
            Discount = None
        # 根据物流方式编号和目的国家编号去查询基本运费计算规则
        try:
            t_cfg_b_emsfare_country_obj = t_cfg_b_emsfare_country.objects.get(country_code=DestinationCountryCode,
                                                                              logisticwaycode=waycode)
            BaseMoney = float(t_cfg_b_emsfare_country_obj.BaseMoney)
            BeginWeight = float(t_cfg_b_emsfare_country_obj.BeginWeight)
            BeginMoney = float(t_cfg_b_emsfare_country_obj.BeginMoney)
            AddWeight = float(t_cfg_b_emsfare_country_obj.AddWeight)
            AddMoney = float(t_cfg_b_emsfare_country_obj.AddMoney)
        except:
            BaseMoney = None
            BeginWeight = None
            BeginMoney = None
            AddWeight = None
            AddMoney = None
        #计算成本价+运费
        extra_Weight = None
        if Weight <= BeginWeight:
            sum_money = (BaseMoney + BeginMoney) * Discount / 100.0 + Money
            params_flow = {'flag': 01, 'BaseMoney': BaseMoney, 'BeginMoney': BeginMoney, 'Discount': Discount,
                            'Money': Money}
        else:
            extra_Weight = Weight - BeginWeight
            sum_money = (BaseMoney + BeginMoney + extra_Weight * AddMoney / AddWeight) * (Discount / 100.0) + Money
            params_flow = {'flag': 02, 'BaseMoney': BaseMoney, 'BeginMoney': BeginMoney, 'extra_Weight': extra_Weight,
                       'AddMoney': AddMoney, 'AddWeight': AddWeight,
                       'Discount': Discount, 'Money': Money}
        #计算利润率
        profitRate = (1- kickback/100 - sum_money/ExchangeRate_USD/sellingPrice)*10.0*10.0
        profitRate = round(profitRate, 2)
        #获取人民币以及目标国家货币价值
        sellingPrice_china = sellingPrice * ExchangeRate_USD
        sellingPrice_destination = sellingPrice_china / ExchangeRate
        params = {'sellingPrice_destination': sellingPrice_destination, 'sellingPrice_china': sellingPrice_china,
                  'logisticName': logisticName, 'CURRENCYCODE': CURRENCYCODE,'ExchangeRate_USD':ExchangeRate_USD,'BaseMoney':BaseMoney,'BeginMoney':BeginMoney,'extra_Weight':extra_Weight,
                  'AddMoney':AddMoney,'AddWeight':AddWeight,'Discount':Discount,'Money':Money,'sum_money':sum_money,'sellingPrice':sellingPrice,
                  'kickback': kickback, 'ExchangeRate': ExchangeRate, 'Discount': Discount,'profitRate':profitRate,'params_flow':params_flow}
        return params
