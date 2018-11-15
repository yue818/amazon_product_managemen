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
from skuapp.table.t_cfg_standard_small import *
from skuapp.table.t_cfg_standard_large import *
from skuapp.table.t_cfg_standard_large_small import *
from skuapp.table.t_cfg_category import *
from pyapp.models import b_goods as py_b_goods
from django.contrib import messages
import math

from __init__ import *

class calculate_price():
    def __init__(self,SKU,Money=None,Weight=None):
        self.SKU = SKU
        self.Money = Money
        self.Weight = Weight
        if not Money:
            try:
                b_goods_obj = py_b_goods.objects.get(SKU=SKU)
                self.Money = str(b_goods_obj.CostPrice)
            except:
                self.Money = None
        if not Weight:
            try:
                b_goods_obj = py_b_goods.objects.get(SKU=SKU)
                self.Weight = str(b_goods_obj.Weight)
            except:
                self.Weight = None

    # 计算售价
    # Weight 商品原始克重(g)
    # Money  商品原始成本(人民币)
    # profitRate 利润率 默认0
    # 返回三种不同货币类型的售价,数据类型dic
    def calculate_selling_price(self,profitRate,platformCountryCode='JOOM-RUS', DestinationCountryCode='RUS',PackWeight=None,LargeCode=None,SmallCode=None,kb=None,category=None,sb_discount=None,bcd_rate=None,yj_rate=None,xss_rate=None,Money=None,Weight=None):
        try:
            Money = float(self.Money)
            Weight = float(self.Weight)
        except:
            Money = float(Money)
            Weight = float(Weight)
        SKU_Weight = Weight
        if platformCountryCode == 'AMAZON-FBA':
            Weight = float(PackWeight)
        profitRate = float(profitRate)

        error_info = {'error_code':200,'error_info':'信息获取成功!'}
        # 根据页面的目的地国家和平台国家编号去找物流方式编号
        t_cfg_b_emsfare2_obj = t_cfg_b_emsfare2.objects.get(platform_country_code=platformCountryCode, countrycode=DestinationCountryCode)
        standard_id = int(t_cfg_b_emsfare2_obj.standard_id)
        category_id = int(t_cfg_b_emsfare2_obj.category_id)
        price_point = float(t_cfg_b_emsfare2_obj.price_point)
        if category_id == 0:
            logisticwaycode_expression = str(t_cfg_b_emsfare2_obj.logisticwaycode)
            logisticwaycode_desc = t_cfg_b_emsfare2_obj.logisticwaycode_desc
        else:
            try:
                t_cfg_category_obj = t_cfg_category.objects.get(category_code=category)
                logisticwaycode_expression = str(t_cfg_category_obj.logisticwaycode)
                logisticwaycode_desc = t_cfg_category_obj.logisticwaycode_desc
            except:
                logisticwaycode_expression = str(t_cfg_b_emsfare2_obj.logisticwaycode)
                logisticwaycode_desc = t_cfg_b_emsfare2_obj.logisticwaycode_desc
        scope = {'sell_price':0,'Weight':Weight}
        exec(logisticwaycode_expression,scope)
        logisticwaycode = scope['waycode']
        #根据当前平台国家编号获取当前货币编号以及平台扣点
        if kb is None or kb.strip() == '':
            kickback = float(t_cfg_b_emsfare2_obj.kickback)
        else:
            kickback = float(kb)
        CURRENCYCODE = None
        basefee = None

        #针对FBA特性，开放一个尾程费用
        if standard_id == 0:
            price_standard = 0
            getprice_standard_desc = ''
        else:
            try:
                t_cfg_standard_large_small_obj = t_cfg_standard_large_small.objects.get(standard_id=standard_id,standard_large_code=LargeCode,standard_small_code=SmallCode)
                CURRENCYCODE_standard = t_cfg_standard_large_small_obj.CURRENCYCODE
                getprice_standard = t_cfg_standard_large_small_obj.getprice
                getprice_standard_desc = t_cfg_standard_large_small_obj.getprice_desc
                scope_standard = {'Weight': Weight}
                exec(getprice_standard, scope_standard)
                price_standard = scope_standard['Price']
                ex_standard = t_cfg_b_currencycode.objects.get(CURRENCYCODE=CURRENCYCODE_standard).ExchangeRate
                price_standard = price_standard * float(ex_standard) #CNY
                #print '---------------------------------------%s'%price_standard #15.183
            except:
                price_standard = 0
                getprice_standard_desc = ''

        try:
            t_cfg_platform_country_obj = t_cfg_platform_country.objects.get(platform_country_code=platformCountryCode)
            #kickback = float(t_cfg_platform_country_obj.kickback)
            basefee = float(t_cfg_platform_country_obj.basefee)
            if DestinationCountryCode == 'GER':
                basefee = basefee + 0.05
            t_cfg_b_country_obj = t_cfg_b_country.objects.get(country_code=DestinationCountryCode)
            CURRENCYCODE = t_cfg_b_country_obj.CURRENCYCODE
            CURRENCYCODE_D = CURRENCYCODE
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
        sellingPrice1 = round(sellingPrice_us, 3)
        params_flow1 = {'flag':01,'logisticwaycode_desc':logisticwaycode_desc,'getprice_desc':getprice_desc,'sellingPrice1':sellingPrice1,'price_yf':price_yf,'fd_money':fd_money,'Discount':Discount,'Money':Money,'basefee':basefee,'ExchangeRate_USD':ExchangeRate_USD,'profitRate':profitRate,'kickback':kickback,'logisticwaycode_expression':logisticwaycode_expression}
        #二次算价重新给域赋值
        for i in range(0,2):
            sum_price_tw = 0
            if (sellingPrice1 >= price_point and price_point != 0) or platformCountryCode == 'JOOM-RUS':
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

            if price_standard != 0:
                sku_count = math.ceil(Weight*1000/SKU_Weight)
                sum_price_tw = float((price_yf + fd_money)/sku_count + price_standard)
                sellingPrice_destination = (sum_price_tw * Discount / 100 + Money + basefee) / ExchangeRate / (1 - profitRate / 100 - kickback / 100)
            
            #补充额外费用
            try:
                extra_id = str(cfg_b_emsfare2[platformCountryCode+'_'+DestinationCountryCode+ '_extra_id'])
                if extra_id != '0':
                    get_fba_price_expression = str(cfg_extra_fee[extra_id+'_get_fba_price'])
                    get_js_price_expression = str(cfg_extra_fee[extra_id+'_get_js_price'])
                    #print '---------------------sb---------------%s'%sb_discount
                    if sb_discount is None or sb_discount == '':
                        sb_discount = cfg_extra_fee[extra_id+'_sb_discount']
                    #print '---------------------sb2---------------%s'%sb_discount
                    if bcd_rate is None or bcd_rate == '':
                        bcd_rate = cfg_extra_fee[extra_id+'_bcd_rate']
                    if yj_rate is None or yj_rate == '':
                        yj_rate = cfg_extra_fee[extra_id+'_yj_rate']
                    if xss_rate is None or xss_rate == '':
                        xss_rate = cfg_extra_fee[extra_id+'_xss_rate']
                    sb_discount = float(sb_discount)
                    bcd_rate = float(bcd_rate)
                    yj_rate = float(yj_rate)
                    xss_rate = float(xss_rate)
                    CURRENCYCODE_extra = str(cfg_extra_fee[extra_id+'_CURRENCYCODE'])
                    ExchangeRate_extra = float(cfg_b_currencycode[CURRENCYCODE_extra])
                    scope5 = {'Weight':Weight}
                    exec(get_fba_price_expression,scope5)
                    price_extra_fba = float(scope5['Price'])
            
                    price_extra_bcd = Money * sb_discount/100 * bcd_rate/100 * 1.1
            
        
                    price_extra_all_des = price_extra_fba + price_extra_bcd/ExchangeRate_extra #目的地货币
                    sellingPrice_destination = ((price_yf+fd_money) * Discount / 100 + Money + price_extra_all_des + basefee) / ExchangeRate / (1 - profitRate / 100 - kickback / 100)
                    scope6 = {'Price':sellingPrice_destination}
                    exec(get_js_price_expression,scope6)
                    sellingPrice_destination = float(scope6['Price'])
                    price_extra_gst = sellingPrice_destination-sellingPrice_destination/(1+xss_rate/100)
                    price_extra_yj = sellingPrice_destination * yj_rate/100 * 1.18
                    price_extra_all_des = price_extra_gst + price_extra_yj + price_extra_fba + price_extra_bcd/ExchangeRate_extra
                    sellingPrice_destination = ((price_yf+fd_money) * Discount / 100 + Money + price_extra_all_des + basefee) / ExchangeRate / (1 - profitRate / 100 - kickback / 100)
            except:
                pass

            sellingPrice_china = sellingPrice_destination * ExchangeRate
            sellingPrice_us = sellingPrice_destination * ExchangeRate / ExchangeRate_USD
            sellingPrice2 = round(sellingPrice_us, 2)
        
            if price_standard == 0:
                params_flow2 = {'flag':02,'logisticwaycode_desc':logisticwaycode_desc,'getprice_desc':getprice_desc,'price_yf':price_yf,'fd_money':fd_money,'Discount':Discount,'Money':Money,'basefee':basefee,'ExchangeRate_USD':ExchangeRate_USD,'profitRate':profitRate,'kickback':kickback,'logisticwaycode_expression':logisticwaycode_expression}
            else:
                standard_large_desc = t_cfg_standard_large.objects.get(standard_id=standard_id,standard_large_code=LargeCode).standard_large_desc 
                standard_small_desc = t_cfg_standard_small.objects.get(standard_id=standard_id,standard_small_code=SmallCode).standard_small_desc
                params_flow3 = {'flag':03,'logisticwaycode_desc':logisticwaycode_desc,'standard_large_desc':standard_large_desc,'getprice_standard_desc':getprice_standard_desc,'standard_small_desc':standard_small_desc,'getprice_desc':getprice_desc,'sum_price_tw':sum_price_tw,'Discount':Discount,'Money':Money,'basefee':basefee,'ExchangeRate_USD':ExchangeRate_USD,'profitRate':profitRate,'kickback':kickback,'logisticwaycode_expression':logisticwaycode_expression}
            #保留俩位小数点
            sellingPrice_destination = round(sellingPrice_destination, 2)
            sellingPrice_china = round(sellingPrice_china, 2)
            sellingPrice_us = round(sellingPrice_us, 2)
            if platformCountryCode == 'JOOM-RUS' and sellingPrice_us >= 5:
                sellingPrice1 = sellingPrice_us
            else:
                break
        
        #sellingPrice 最终售价,同时获取 logisticName物流方式,kickback平台扣点,ExchangeRate汇率,Discount物流折扣 以dic形式返回=>
        if price_standard != 0:
            params = {'sellingPrice_destination':sellingPrice_destination,'sellingPrice_china':sellingPrice_china,'sellingPrice_us':sellingPrice_us,'logisticName':logisticName,'CURRENCYCODE':CURRENCYCODE_D,'kickback':kickback,'ExchangeRate':ExchangeRate,'Discount':Discount,'params_flow':params_flow3,'sb_discount':sb_discount,'bcd_rate':bcd_rate,'yj_rate':yj_rate,'xss_rate':xss_rate}
        else:
            #if platformCountryCode == 'JOOM-RUS':
            #    if sellingPrice1 == sellingPrice2:
            #        params = {'sellingPrice_destination':sellingPrice_destination,'sellingPrice_china':sellingPrice_china,'sellingPrice_us':sellingPrice1,'logisticName':logisticName,'CURRENCYCODE':CURRENCYCODE_D,'kickback':kickback,'ExchangeRate':ExchangeRate,'Discount':Discount,'params_flow':params_flow1,'sb_discount':sb_discount,'bcd_rate':bcd_rate,'yj_rate':yj_rate,'xss_rate':xss_rate}
            #    else:
            #        params = {'sellingPrice_destination':sellingPrice_destination,'sellingPrice_china':sellingPrice_china,'sellingPrice_us':sellingPrice_us,'logisticName':logisticName,'CURRENCYCODE':CURRENCYCODE_D,'kickback':kickback,'ExchangeRate':ExchangeRate,'Discount':Discount,'params_flow':params_flow2,'params_flow1':params_flow1,'sb_discount':sb_discount,'bcd_rate':bcd_rate,'yj_rate':yj_rate,'xss_rate':xss_rate}
            #else:
            if sellingPrice1 < price_point or price_point == 0:
                params = {'sellingPrice_destination':sellingPrice_destination,'sellingPrice_china':sellingPrice_china,'sellingPrice_us':sellingPrice1,'logisticName':logisticName,'CURRENCYCODE':CURRENCYCODE_D,'kickback':kickback,'ExchangeRate':ExchangeRate,'Discount':Discount,'params_flow':params_flow1,'sb_discount':sb_discount,'bcd_rate':bcd_rate,'yj_rate':yj_rate,'xss_rate':xss_rate}
            else:
                params = {'sellingPrice_destination':sellingPrice_destination,'sellingPrice_china':sellingPrice_china,'sellingPrice_us':sellingPrice_us,'logisticName':logisticName,'CURRENCYCODE':CURRENCYCODE_D,'kickback':kickback,'ExchangeRate':ExchangeRate,'Discount':Discount,'params_flow':params_flow2,'params_flow1':params_flow1,'sb_discount':sb_discount,'bcd_rate':bcd_rate,'yj_rate':yj_rate,'xss_rate':xss_rate}
        return params

    # 计算利润率
    # platformCountryCode=t_cfg_b_emsfare.platform_country_code
    # Weight 商品原始克重(g)
    # Money  商品原始成本(人民币)
    # sellingPrice 售价(人民币，显示的是加入汇率计算)
    # 返回profitRate利润率(百分制,15就是 15%)
    #(成本(￥)+运费(￥))/汇率/(1-利润率-平台扣点比率) = 最终售价(目标币种)
    def calculate_profitRate(self, sellingPrice,platformCountryCode='JOOM-RUS', DestinationCountryCode='RUS',kb=None,price_des=None,currencycode=None,category=None,sb_discount=None,bcd_rate=None,yj_rate=None,xss_rate=None,Money=None,Weight=None):
        try:
            Money = float(self.Money)
            Weight = float(self.Weight)
        except:
            Money = float(Money)
            Weight = float(Weight)
        try:
            if currencycode is None or currencycode.strip() == '':
                sellingPrice = float(sellingPrice)
            else:
                price_des = float(price_des)
                currencycode = str(currencycode)
                ExchangeRate1 = float(cfg_b_currencycode[currencycode])
                ExchangeRate2 = float(cfg_b_currencycode['ExchangeRate_USD'])
                sellingPrice = price_des*ExchangeRate1/ExchangeRate2
        except:
            sellingPrice = -1
        #print '--------------sellprice---------%s'%sellingPrice
        #获取美元与人民币汇率
        try:
            #t_cfg_b_currencycode_obj = t_cfg_b_currencycode.objects.get(CURRENCYCODE='USD')
            #ExchangeRate_USD = float(t_cfg_b_currencycode_obj.ExchangeRate)
            ExchangeRate_USD = cfg_b_currencycode['ExchangeRate_USD']
        except:
            ExchangeRate_USD = None
        #根据当前平台国家编号获取当前货币编号以及平台扣点
        try:
            #t_cfg_platform_country_obj = t_cfg_platform_country.objects.get(platform_country_code=platformCountryCode)
            #basefee = float(t_cfg_platform_country_obj.basefee)
            basefee = float(cfg_platform_country[platformCountryCode])
            if DestinationCountryCode == 'GER':
                basefee = basefee + 0.05
            #t_cfg_b_emsfare2_obj = t_cfg_b_emsfare2.objects.get(platform_country_code=platformCountryCode, countrycode=DestinationCountryCode)
            #kickback = float(t_cfg_b_emsfare2_obj.kickback)
            if kb is None or kb.strip() == '':
                kickback = float(cfg_b_emsfare2[platformCountryCode+'_'+DestinationCountryCode+'_kickback'])
            else:
                kickback = float(kb)           

            #t_cfg_b_country_obj = t_cfg_b_country.objects.get(country_code=DestinationCountryCode)
            #CURRENCYCODE = t_cfg_b_country_obj.CURRENCYCODE
            CURRENCYCODE = str(cfg_b_country[DestinationCountryCode])

            #ExchangeRate_basefee = t_cfg_b_currencycode.objects.get(CURRENCYCODE=CURRENCYCODE).ExchangeRate
            ExchangeRate_basefee = cfg_b_currencycode[CURRENCYCODE]
            basefee = basefee * float(ExchangeRate_basefee)
        except:
            kickback = None
            CURRENCYCODE = None
            basefee = None
        #根据货币编号获取人民币汇率
        try:
            #t_cfg_b_currencycode_obj = t_cfg_b_currencycode.objects.get(CURRENCYCODE=CURRENCYCODE)
            #ExchangeRate = float(t_cfg_b_currencycode_obj.ExchangeRate)
            ExchangeRate = float(cfg_b_currencycode[CURRENCYCODE])
        except:
            ExchangeRate = None
       # 根据页面的目的地国家和平台国家编号去找默认物流方式编号，最大价格限制以及超过最大价格后采取的新的物流方式编号
        #t_cfg_b_emsfare2_obj = t_cfg_b_emsfare2.objects.get(platform_country_code=platformCountryCode, countrycode=DestinationCountryCode)
        #logisticwaycode_expression = str(t_cfg_b_emsfare2_obj.logisticwaycode)
        category_id = int(cfg_b_emsfare2[platformCountryCode+'_'+DestinationCountryCode+'_category_id'])
        if category_id == 0:
            logisticwaycode_expression = str(cfg_b_emsfare2[platformCountryCode+'_'+DestinationCountryCode+'_logisticway'])
            logisticwaycode_desc = str(cfg_b_emsfare2[platformCountryCode+'_'+DestinationCountryCode+'_logisticway_desc'])
        else:
            logisticwaycode_expression = str(cfg_category[str(category_id)+'_'+str(category)])
            logisticwaycode_desc = str(cfg_category[str(category_id)+'_'+str(category)+'_desc'])
        scope = {'sell_price':sellingPrice,'Weight':Weight}
        exec(logisticwaycode_expression,scope)
        waycode = scope['waycode']
                
        try:
            #t_cfg_b_logisticway_obj = t_cfg_b_logisticway.objects.get(code=waycode)
            #logisticName = t_cfg_b_logisticway_obj.name
            #Discount = float(t_cfg_b_logisticway_obj.Discount)
            logisticName = cfg_b_logisticway[waycode + '_name']
            Discount = cfg_b_logisticway[waycode + '_Discount']
        except:
            logisticName = None
            Discount = None
        # 根据物流方式编号和目的国家编号去查询基本运费计算规则
        #t_cfg_b_emsfare_country2_obj = t_cfg_b_emsfare_country2.objects.get(country_code=DestinationCountryCode, logisticwaycode=waycode)
        #getprice_expression = t_cfg_b_emsfare_country2_obj.getprice
        getprice_expression = str(cfg_b_emsfare_country2[DestinationCountryCode+'_'+waycode+'_getprice'])
        scope2 = {'Weight': Weight} 
        exec(getprice_expression,scope2)
        price_yf = scope2['Price']
        #Bracketid = t_cfg_b_emsfare_country2_obj.Bracketid
        Bracketid = cfg_b_emsfare_country2[DestinationCountryCode+'_'+waycode+'_bracketid']
        if Bracketid is None or Bracketid == '' or Bracketid == 0:
            fd_money = 0
        else:
            #二次算价获取分档运费
            try:
                fd_money     = float(t_cfg_bracket.objects.filter(bracketid=Bracketid, weight__gte=Weight).order_by('weight').values_list('money', flat=True)[:1][0])
                CURRENCYCODE = str(t_cfg_bracket.objects.filter(bracketid=Bracketid,weight__gte=Weight).order_by('weight').values_list('CURRENCYCODE',flat=True)[:1][0])
                #ExchangeRate = t_cfg_b_currencycode.objects.get(CURRENCYCODE=CURRENCYCODE).ExchangeRate
                ExchangeRate = float(cfg_b_currencycode[CURRENCYCODE])
                fd_money     = fd_money * ExchangeRate
            except:
                fd_money = 0
        #补充额外费用
        try:
            extra_id = str(cfg_b_emsfare2[platformCountryCode+'_'+DestinationCountryCode+ '_extra_id'])
        except:
            extra_id == '0'
        if extra_id == '0':
            sb_discount = None
            bcd_rate = None
            yj_rate = None
            xss_rate = None
            price_extra_all = 0
        else:
            get_fba_price_expression = str(cfg_extra_fee[extra_id+'_get_fba_price'])
            get_js_price_expression = str(cfg_extra_fee[extra_id+'_get_js_price'])
            get_qg_price_expression = str(cfg_extra_fee[extra_id+'_get_qg_price'])
            #print '---------------------sb---------------%s'%sb_discount
            if sb_discount is None or sb_discount == '':
                sb_discount = cfg_extra_fee[extra_id+'_sb_discount']
            #print '---------------------sb2---------------%s'%sb_discount
            if bcd_rate is None or bcd_rate == '':
                bcd_rate = cfg_extra_fee[extra_id+'_bcd_rate']
            if yj_rate is None or yj_rate == '':
                yj_rate = cfg_extra_fee[extra_id+'_yj_rate']
            if xss_rate is None or xss_rate == '':
                xss_rate = cfg_extra_fee[extra_id+'_xss_rate']
            sb_discount = float(sb_discount)
            bcd_rate = float(bcd_rate)
            yj_rate = float(yj_rate)
            xss_rate = float(xss_rate)
            CURRENCYCODE_extra = str(cfg_extra_fee[extra_id+'_CURRENCYCODE'])
            ExchangeRate_extra = float(cfg_b_currencycode[CURRENCYCODE_extra])
            #卢比
            scope3 = {'Weight':Weight}
            exec(get_fba_price_expression,scope3)
            price_extra_fba = float(scope3['Price'])
            #print '-----------price_extra_fba-----------%s'%price_extra_fba
            #print '-----------price_des-----------%s'%price_des
            if price_des is None:
                price_des = sellingPrice * ExchangeRate_USD / ExchangeRate_extra
            scope4 = {'Price':price_des}
            exec(get_js_price_expression,scope4)
            price_extra_js = float(scope4['Price'])*1.18
            scope5 = {'Price':price_des}
            exec(get_qg_price_expression,scope5)
            price_extra_qg = float(scope5['Price'])
            #print '-----------price_extra_js-----------%s'%price_extra_js
            price_extra_bcd = Money/ExchangeRate_extra * sb_discount/100 * bcd_rate/100 * 1.1
            #print '-----------price_extra_bcd-----------%s'%price_extra_bcd
            price_extra_gst = price_des-price_des/(1+xss_rate/100)
            #print '-----------price_extra_gst-----------%s'%price_extra_gst
            price_extra_yj = price_des * yj_rate/100 * 1.18
            #print '-----------price_extra_yj-----------%s'%price_extra_yj      
            price_extra_all = price_extra_fba + price_extra_js + price_extra_bcd + price_extra_gst + price_extra_yj + price_extra_qg
            #print '-----------price_extra_qg-----------%s'%price_extra_qg 
            price_extra_all = price_extra_all * ExchangeRate_extra
        
        
        
        
        sum_money = (price_yf + fd_money) * Discount / 100.0 + Money + basefee + price_extra_all
        print '-----------sum_money-----------%s'%sum_money
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
                  'kickback': kickback, 'ExchangeRate': ExchangeRate, 'Discount': Discount,'profitRate':profitRate,'sb_discount':sb_discount,'bcd_rate':bcd_rate,'yj_rate':yj_rate,'xss_rate':xss_rate,'logisticwaycode_desc':logisticwaycode_desc}
        return params
