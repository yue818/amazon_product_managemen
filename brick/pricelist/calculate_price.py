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
        try:
            sku_number = SKU.split('*')
            if len(sku_number) == 1:
                self.SKU = SKU
                self.num = 1
            elif len(sku_number) == 2:
                self.SKU = sku_number[0]
                self.num = int(sku_number[1])
            else:
                pass
        except:
            self.SKU = SKU

        self.Money = Money
        self.Weight = Weight

        if not Money:
            try:
                b_goods_obj = py_b_goods.objects.get(SKU=self.SKU)
                self.Money = str(b_goods_obj.CostPrice*self.num)
            except:
                self.Money = None
        if not Weight:
            try:
                b_goods_obj = py_b_goods.objects.get(SKU=self.SKU)
                self.Weight = str(b_goods_obj.Weight*self.num)
            except:
                self.Weight = None

    # 计算售价
    # Weight 商品原始克重(g)
    # Money  商品原始成本(人民币)
    # profitRate 利润率 默认0
    # 返回三种不同货币类型的售价,数据类型dic
    def calculate_selling_price(self,profitRate,platformCountryCode='JOOM-RUS', DestinationCountryCode='RUS',PackWeight=None,LargeCode=None,SmallCode=None,kb=None,category=None,sb_discount=None,bcd_rate=None,yj_rate=None,xss_rate=None,Money=None,Weight=None,logistic_way=None,cp=None):
        try:
            Money = float(self.Money)
            Weight = float(self.Weight)
        except:
            Money = float(Money)
            Weight = float(Weight)
        #SKU_Weight = Weight
        #if platformCountryCode == 'AMAZON-FBA':
            #Weight = float(PackWeight)
        #针对AMAZON-FBA的实重和抛重以及轻小件商品计划
        fba_info = {}
        fba_info['xxj'] = '不支持'
        if PackWeight and PackWeight != 0 and PackWeight != 20:
            PackWeight = str(PackWeight)
            if PackWeight.find("*") >=0:
                cm_list = []
                cm_list.append(float(PackWeight.split("*")[0]))
                cm_list.append(float(PackWeight.split("*")[1]))
                cm_list.append(float(PackWeight.split("*")[2]))
                cm_list.sort()
                cm_list.reverse()
                cm1 = cm_list[0]
                cm2 = cm_list[1]
                cm3 = cm_list[2]
                try:            
                    tj_weight = cm1*cm2*cm3/6
                except:
                    tj_weight = 0
            else:
                tj_weight = float(PackWeight)
            if DestinationCountryCode == 'US' and cm1 <= 40.64 and cm2 <=22.86 and cm3 <= 10.16 and Weight < 425.24:
                price_xxj_yf = (1.75 + math.ceil(0.035 * Weight)*0.11)*6.8
                fba_info['xxj'] = u'价格不超过 $5.00 的商品收取 $0.80 的订单处理费，对价格超过 $5.00 的商品收取 $1.00 的订单处理费。取件及包装费将按每件商品 $0.75 的费率收取。首重和续重费将按每盎司 $0.11 的费率收取'
            elif DestinationCountryCode == 'UK':
                if cm1 <= 23 and cm2 <=15.5 and cm3 <= 0.4 and Weight < 92:
                    price_xxj_yf = 0.6*8.7
                    fba_info['xxj'] = u'小号信封每件£0.60,注意：价格不超过 £9！'
                elif cm1 <= 30 and cm2 <=22.4 and cm3 <= 2.4 and Weight < 225:
                    price_xxj_yf = 0.8*8.7
                    fba_info['xxj'] = u'大号信封每件£0.80,注意：价格不超过 £9！'
            elif DestinationCountryCode == 'GER':
                if cm1 <= 21.5 and cm2 <=10.5 and cm3 <= 0.6 and Weight < 50:
                    price_xxj_yf = 1.10*7.8
                    fba_info['xxj'] = u'小号信封每件€1.10,注意：价格不超过 €10！'
                elif cm1 <= 33.5 and cm2 <=23 and cm3 <= 2.8 and Weight < 225:
                    price_xxj_yf = 1.35*7.8
                    fba_info['xxj'] = u'大号信封每件€1.35,注意：价格不超过 €10！'
                elif cm1 <= 33.5 and cm2 <=23 and cm3 <= 4.6 and Weight < 225:
                    price_xxj_yf = 1.7*7.8
                    fba_info['xxj'] = u'超大号信封每件€1.70,注意：价格不超过 €10！'
            if Weight > tj_weight:
                Weight = Weight
                fba_info['weight_status'] = u'实重'
            else:
                Weight = tj_weight
                fba_info['weight_status'] = u'抛重'            
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
        if platformCountryCode =='AMAZON-FBA':
            logisticwaycode = logistic_way
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
            price_standard_efn = 0
            price_standard_efn_des = 0
            getprice_standard_desc = ''
        else:
            try:
                #print '---standard_id---%s----standard_large_code---%s------standard_small_code---%s---'%(standard_id,LargeCode,SmallCode)
                t_cfg_standard_large_small_obj = t_cfg_standard_large_small.objects.get(standard_id=standard_id,standard_large_code=LargeCode,standard_small_code=SmallCode)
                CURRENCYCODE_standard = t_cfg_standard_large_small_obj.CURRENCYCODE
                getprice_standard = t_cfg_standard_large_small_obj.getprice
                getprice_standard_desc = t_cfg_standard_large_small_obj.getprice_desc
                scope_standard = {'Weight': Weight}
                exec(getprice_standard, scope_standard)
                price_standard = scope_standard['Price']
                ex_standard = t_cfg_b_currencycode.objects.get(CURRENCYCODE=CURRENCYCODE_standard).ExchangeRate
                price_standard = price_standard * float(ex_standard) #CNY
                if DestinationCountryCode == 'US':
                    if cp == 'FZ':
                        price_standard = price_standard + 0.4 * float(ex_standard)
                    elif cp == 'FFZ':
                        price_standard = price_standard
                #print '---------------------------------------%s'%price_standard #15.183
            except:
                price_standard = 0
                getprice_standard_desc = ''
            try:
                price_standard_efn = scope_standard['Price_efn']
                price_standard_efn_des = price_standard_efn
                price_standard_efn = price_standard_efn * float(ex_standard) #CNY
            except:
                price_standard_efn = 0
                price_standard_efn_des = 0

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
        price_yf = 0
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
                        
                sum_price_tw = float((price_yf + fd_money) + price_standard)
                sellingPrice_destination = (sum_price_tw * Discount / 100 + Money + basefee) / ExchangeRate / (1 - profitRate / 100 - kickback / 100)
                price_fba_yj = sellingPrice_destination * kickback / 100
                
                sum_price_tw_efn = float((price_yf + fd_money) + price_standard_efn)
                sellingPrice_destination_efn = (sum_price_tw_efn * Discount / 100 + Money + basefee) / ExchangeRate / (1 - profitRate / 100 - kickback / 100)
                price_efn_yj = sellingPrice_destination * kickback / 100
                sellingPrice_destination_efn_ch = sellingPrice_destination_efn*ExchangeRate
                price_efn_yj_ch = price_efn_yj*ExchangeRate
                #轻小件提示
                try:
                    sum_price_tw2 = float((price_xxj_yf + fd_money) + price_yf)
                    sellingPrice_destination2 = (sum_price_tw2 * Discount / 100 + Money + basefee) / ExchangeRate / (1 - profitRate / 100 - kickback / 100)
                    #针对美国FBA二次算价
                    if sellingPrice_destination2 > 5 and DestinationCountryCode == 'US':
                        sum_price_tw2 = sum_price_tw2 + 0.2 * 6.8
                    sellingPrice_destination2 = (sum_price_tw2 * Discount / 100 + Money + basefee) / ExchangeRate / (1 - profitRate / 100 - kickback / 100)
                except:
                    sum_price_tw2 = None
                    sellingPrice_destination2 = None
            
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
                params_flow3 = {'flag':03,'price_standard_efn_des':round(price_standard_efn_des,2),'price_standard_efn':round(price_standard_efn,2),'sellingPrice_destination_efn':round(sellingPrice_destination_efn,2),'sellingPrice_destination_efn_ch':round(sellingPrice_destination_efn_ch,2),'price_efn_yj':round(price_efn_yj,2),'price_efn_yj_ch':round(price_efn_yj_ch,2),'logisticwaycode_desc':logisticwaycode_desc,'standard_large_desc':standard_large_desc,'getprice_standard_desc':getprice_standard_desc,'standard_small_desc':standard_small_desc,'getprice_desc':getprice_desc,'sum_price_tw':round(sum_price_tw,2),'Discount':Discount,'Money':Money,'basefee':basefee,'ExchangeRate_USD':ExchangeRate_USD,'profitRate':profitRate,'kickback':kickback,'price_yf':round(price_yf,2),'price_yf_us':round(price_yf/ExchangeRate_USD,2),'price_yf_des':round(price_yf/ExchangeRate,2),'price_standard_des':round(price_standard/ExchangeRate,2),'price_standard':round(price_standard,2),'price_fba_yj_des':round(price_fba_yj,2),'price_fba_yj':round(price_fba_yj*ExchangeRate,2),'fba_info':fba_info}
                params_flow3['sellingPrice2_qxj']='不支持'
                params_flow3['sellingPrice_china_qxj']='不支持'
                params_flow3['price_fba_yj2']='不支持'
                params_flow3['price_fba_yj2_china']='不支持'
                params_flow3['price_xxj_yf']='不支持' #人民币
                params_flow3['price_xxj_yf_us']='不支持' #美元
                params_flow3['sellingPrice_des_qxj']='不支持'
                params_flow3['price_fba_yj2_des']='不支持'
                params_flow3['price_xxj_yf_des']='不支持'
                if sellingPrice_destination2:
                    sellingPrice_china_qxj = sellingPrice_destination2 * ExchangeRate
                    sellingPrice_us_qxj = sellingPrice_destination2 * ExchangeRate / ExchangeRate_USD
                    sellingPrice2_qxj = round(sellingPrice_us_qxj, 2)
                    params_flow3['sellingPrice2_qxj']=round(sellingPrice2_qxj,2)
                    params_flow3['sellingPrice_china_qxj']=round(sellingPrice_china_qxj,2)
                    params_flow3['sellingPrice_des_qxj']=round(sellingPrice_china_qxj/ExchangeRate,2)
                    #佣金
                    params_flow3['price_fba_yj2']=round(sellingPrice2_qxj * kickback/100,2)
                    params_flow3['price_fba_yj2_china']=round(sellingPrice_china_qxj * kickback/100,2)
                    params_flow3['price_fba_yj2_des']=round(sellingPrice_destination2 * kickback/100,2)
                    #尾程
                    params_flow3['price_xxj_yf']=round(price_xxj_yf,2) #人民币
                    params_flow3['price_xxj_yf_us']=round(price_xxj_yf/ExchangeRate_USD,2) #美元
                    params_flow3['price_xxj_yf_des']=round(price_xxj_yf/ExchangeRate,2) #目标
                     
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
        # print '-----------sum_money-----------%s'%sum_money
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
        
    def batch_calculate_selling_price(self,profitRate,platformCountryCode='JOOM-RUS', DestinationCountryCode='RUS',PackWeight=None,LargeCode=None,SmallCode=None,kb=None,category=None,sb_discount=None,bcd_rate=None,yj_rate=None,xss_rate=None,Money=None,Weight=None,logistic_way=None):
        try:
            Money = float(self.Money)
            Weight = float(self.Weight)
        except:
            Money = float(Money)
            Weight = float(Weight)          
        if PackWeight and PackWeight != 0 and PackWeight != 20:
            PackWeight = str(PackWeight)
            if PackWeight.find("*") >=0:
                try:
                    tj_weight = float(PackWeight.split("*")[0])*float(PackWeight.split("*")[1])*float(PackWeight.split("*")[2])/6
                except:
                    tj_weight = 0
            else:
                tj_weight = PackWeight
            if Weight > tj_weight:
                Weight = Weight
            else:
                Weight = tj_weight
        profitRate = float(profitRate)
        error_info = {'error_code':200,'error_info':'信息获取成功!'}
        # 根据页面的目的地国家和平台国家编号去找物流方式编号
        standard_id = cfg_b_emsfare2[platformCountryCode+'_'+DestinationCountryCode+ '_standard_id']
        category_id = cfg_b_emsfare2[platformCountryCode+'_'+DestinationCountryCode+ '_category_id']
        price_point = cfg_b_emsfare2[platformCountryCode+'_'+DestinationCountryCode+ '_price_point']
        if category_id == 0:
            logisticwaycode_expression = str(cfg_b_emsfare2[platformCountryCode+'_'+DestinationCountryCode+ '_logisticway'])
            logisticwaycode_desc = str(cfg_b_emsfare2[platformCountryCode+'_'+DestinationCountryCode+ '_logisticway_desc'])
        else:
            try:
                logisticwaycode_expression = str(cfg_category[str(category_id)+'_'+str(category)])
                logisticwaycode_desc = str(cfg_category[str(category_id)+'_'+str(category)+'_desc'])
            except:
                logisticwaycode_expression = str(cfg_b_emsfare2[platformCountryCode+'_'+DestinationCountryCode+ '_logisticway'])
                logisticwaycode_desc = str(cfg_b_emsfare2[platformCountryCode+'_'+DestinationCountryCode+ '_logisticway_desc'])
        scope = {'sell_price':0,'Weight':Weight}
        exec(logisticwaycode_expression,scope)
        logisticwaycode = scope['waycode']
        if platformCountryCode =='AMAZON-FBA':
            logisticwaycode = logistic_way
        #根据当前平台国家编号获取当前货币编号以及平台扣点
        if kb is None or kb.strip() == '':
            kickback = float(cfg_b_emsfare2[platformCountryCode+'_'+DestinationCountryCode+ '_kickback'])
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
                CURRENCYCODE_standard = cfg_standard_large_small[str(standard_id)+str(LargeCode)+str(SmallCode)+'_CURRENCYCODE']
                getprice_standard = cfg_standard_large_small[str(standard_id)+str(LargeCode)+str(SmallCode)+'_getprice']
                getprice_standard_desc = cfg_standard_large_small[str(standard_id)+str(LargeCode)+str(SmallCode)+'_getprice_desc']
                scope_standard = {'Weight': Weight}
                exec(getprice_standard, scope_standard)
                price_standard = scope_standard['Price']
                ex_standard = cfg_b_currencycode[CURRENCYCODE_standard]
                price_standard = price_standard * float(ex_standard) #CNY
            except:
                price_standard = 0
                getprice_standard_desc = ''

        try:
            basefee = float(cfg_platform_country[platformCountryCode])
            if DestinationCountryCode == 'GER':
                basefee = basefee + 0.05
            CURRENCYCODE = cfg_b_country[DestinationCountryCode]
            CURRENCYCODE_D = CURRENCYCODE
            ExchangeRate_basefee = cfg_b_currencycode[CURRENCYCODE]
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
            ExchangeRate = float(cfg_b_currencycode[CURRENCYCODE])
        except:
            error_info = {'error_code': 3, 'error_info': '当前货币与人民币汇率 没有配置！'}
            

        #获取美元与人民币汇率
        ExchangeRate_USD = None
        try:
            ExchangeRate_USD = cfg_b_currencycode['ExchangeRate_USD']
        except:
            error_info = {'error_code': 4, 'error_info': '美元与人民币汇率 没有配置！'}
            

        #根据物流方式编号和目的国家编号去查询基本运费计算规则
        price_yf = 0
        try:
            getprice_expression = str(cfg_b_emsfare_country2[DestinationCountryCode+'_'+logisticwaycode+'_getprice'])
            getprice_desc = str(cfg_b_emsfare_country2[DestinationCountryCode+'_'+logisticwaycode+'_getprice_desc'])
            scope2 = {'Weight': Weight} 
            exec(getprice_expression, scope2)
            price_yf = scope2['Price']
            Bracketid = str(cfg_b_emsfare_country2[DestinationCountryCode+'_'+logisticwaycode+'_bracketid'])
        except:
            error_info = {'error_code': 5, 'error_info': '基础费用/初始价格/初始重量/增加价格/增加重量 没有配置！'}
            
        
        #根据一次算价的物流方式得到的外键Bracketid获取分档价格
        if Bracketid != '0':
            try:
                fd_money     = float(t_cfg_bracket.objects.filter(bracketid=Bracketid,weight__gte=Weight).order_by('weight').values_list('money',flat=True)[:1][0])
                CURRENCYCODE = t_cfg_bracket.objects.filter(bracketid=Bracketid,weight__gte=Weight).order_by('weight').values_list('CURRENCYCODE',flat=True)[:1][0]
                ExchangeRate2 = t_cfg_b_currencycode.objects.get(CURRENCYCODE=CURRENCYCODE).ExchangeRate
                fd_money     = fd_money * float(ExchangeRate2)
            except:
                fd_money = 0
        else:
            fd_money = 0

        #一次算价,获取对应物流中文名称以及物流折扣
        logisticName = None
        Discount = None
        try:
            logisticName = cfg_b_logisticway[logisticwaycode+'_name']
            Discount = float(cfg_b_logisticway[logisticwaycode+'_Discount'])
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
                    logisticName = cfg_b_logisticway[pricelimit_logisticwaycode+'_name']
                    Discount = float(cfg_b_logisticway[pricelimit_logisticwaycode+'_Discount'])
                except:
                    logisticName = None
                    Discount = None
                #二次算价获取运费
                getprice_expression = str(cfg_b_emsfare_country2[DestinationCountryCode+'_'+pricelimit_logisticwaycode+'_getprice'])
                getprice_desc = str(cfg_b_emsfare_country2[DestinationCountryCode+'_'+pricelimit_logisticwaycode+'_getprice_desc'])
                scope4 = {'Weight': Weight} 
                exec(getprice_expression,scope4)
                price_yf = scope4['Price']
                Bracketid = str(cfg_b_emsfare_country2[DestinationCountryCode+'_'+logisticwaycode+'_bracketid'])
                #二次算价获取分档运费
                if Bracketid != '0':
                    try:
                        fd_money     = float(t_cfg_bracket.objects.filter(bracketid=Bracketid, weight__gte=Weight).order_by('weight').values_list('money', flat=True)[:1][0])
                        CURRENCYCODE = t_cfg_bracket.objects.filter(bracketid=Bracketid,weight__gte=Weight).order_by('weight').values_list('CURRENCYCODE',flat=True)[:1][0]
                        ExchangeRate2 = t_cfg_b_currencycode.objects.get(CURRENCYCODE=CURRENCYCODE).ExchangeRate
                        fd_money     = fd_money * float(ExchangeRate2)
                    except:
                        fd_money = 0
                else:
                    fd_money = 0

                sellingPrice_destination = ((price_yf+fd_money) * Discount / 100 + Money + basefee) / ExchangeRate / (1 - profitRate / 100 - kickback / 100)  # 目的国家售价

            if price_standard != 0:
                sum_price_tw = float((price_yf + fd_money) + price_standard)
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
            if sellingPrice1 < price_point or price_point == 0:
                params = {'sellingPrice_destination':sellingPrice_destination,'sellingPrice_china':sellingPrice_china,'sellingPrice_us':sellingPrice1,'logisticName':logisticName,'CURRENCYCODE':CURRENCYCODE_D,'kickback':kickback,'ExchangeRate':ExchangeRate,'Discount':Discount,'params_flow':params_flow1,'sb_discount':sb_discount,'bcd_rate':bcd_rate,'yj_rate':yj_rate,'xss_rate':xss_rate}
            else:
                params = {'sellingPrice_destination':sellingPrice_destination,'sellingPrice_china':sellingPrice_china,'sellingPrice_us':sellingPrice_us,'logisticName':logisticName,'CURRENCYCODE':CURRENCYCODE_D,'kickback':kickback,'ExchangeRate':ExchangeRate,'Discount':Discount,'params_flow':params_flow2,'params_flow1':params_flow1,'sb_discount':sb_discount,'bcd_rate':bcd_rate,'yj_rate':yj_rate,'xss_rate':xss_rate}
        return params
        
    def calculate_profitRate_fba(self,sellingPrice,PackWeight,cm,logistic_way,platformCountryCode='AMAZON-FBA', DestinationCountryCode='US',cp=None,kb=None):
        Money = float(self.Money) #成本价
        PackWeight = float(PackWeight)
        sellingPrice = float(sellingPrice)
        #sellingPrice当地货币
        #根据当前平台国家编号获取当前货币编号以及平台扣点
        if kb is None or kb.strip() == '':
            kickback = float(cfg_b_emsfare2[platformCountryCode+'_'+DestinationCountryCode+ '_kickback'])
        else:
            kickback = float(kb)
                         
        #判断抛重(实重)
        cm = str(cm)
        if cm.find("*") >=0:
            cm_list = []
            cm_list.append(float(cm.split("*")[0]))
            cm_list.append(float(cm.split("*")[1]))
            cm_list.append(float(cm.split("*")[2]))
            cm_list.sort()
            cm_list.reverse()
            cm1 = cm_list[0]
            cm2 = cm_list[1]
            cm3 = cm_list[2]
            try:            
                tj_weight = cm1*cm2*cm3/6
            except:
                tj_weight = 0
        else:
            tj_weight = float(PackWeight)
        if PackWeight > tj_weight:
            Weight = PackWeight
        else:
            Weight = tj_weight  
            
            
        #获取头程运费(CNY)
        getprice_expression = str(cfg_b_emsfare_country2[DestinationCountryCode+'_'+logistic_way+'_getprice'])
        scope = {'Weight':PackWeight}
        exec(getprice_expression,scope)
        price_first = float(scope['Price'])
                    
        #获取尾程的  轻小件运费(按实重计算)                                
        if DestinationCountryCode == 'US' and cm1 <= 40.64 and cm2 <=22.86 and cm3 <= 10.16 and PackWeight < 425.24:
            price_xxj_yf = (1.75 + math.ceil(0.035 * PackWeight)*0.11)*6.8
        elif DestinationCountryCode == 'UK':
            if cm1 <= 23 and cm2 <=15.5 and cm3 <= 0.4 and PackWeight < 92:
                price_xxj_yf = 0.6*8.7
            elif cm1 <= 30 and cm2 <=22.4 and cm3 <= 2.4 and PackWeight < 225:
                price_xxj_yf = 0.8*8.7
        elif DestinationCountryCode == 'GER':
            if cm1 <= 21.5 and cm2 <=10.5 and cm3 <= 0.6 and PackWeight < 50:
                price_xxj_yf = 1.10*7.8
            elif cm1 <= 33.5 and cm2 <=23 and cm3 <= 2.8 and PackWeight < 225:
                price_xxj_yf = 1.35*7.8
            elif cm1 <= 33.5 and cm2 <=23 and cm3 <= 4.6 and PackWeight < 225:
                price_xxj_yf = 1.7*7.8
            
        #获取尾程的 FBA运费(按最大值计算)
        result = {}
        circle = (cm_list[1]+cm_list[2])*2 + cm_list[0]
        standard_id = int(t_cfg_b_emsfare2.objects.get(platform_country_code='AMAZON-FBA', countrycode=DestinationCountryCode).standard_id)
        if standard_id == 1:
            if cm_list[0]<=38.1 and cm_list[1]<=30.48 and cm_list[2]<=1.9 and Weight<=340:
                result['bigflag'] = 'FBA-US-M'
                result['smallflag'] = 'M-S'
            elif cm_list[0]<=45.72 and cm_list[1]<=35.56 and cm_list[2]<=20.32 and Weight<=9071.8:
                result['bigflag'] = 'FBA-US-M'
                if Weight <= 454:
                    result['smallflag'] = 'M-L1'
                elif Weight > 454 and Weight <= 908:
                    result['smallflag'] = 'M-L2'
                else:
                    result['smallflag'] = 'M-L3'
            elif cm_list[0]<=152.4 and cm_list[1]<=76.2 and Weight<=31751.4:
                result['bigflag'] = 'FBA-US-L'
                result['smallflag'] = 'L-S'
            elif cm_list[0]<=274.32 and Weight<=68038.8:
                result['bigflag'] = 'FBA-US-L'
                if circle <= 330.2:
                    result['smallflag'] = 'L-M'
                elif circle > 330.2 and circle <=419.1:
                    result['smallflag'] = 'L-L1'
            elif cm_list[0]>274.32 and Weight>68038.8:
                result['bigflag'] = 'FBA-US-L'
                result['smallflag'] = 'L-L2'
        else:
            if cm_list[0]<=20 and cm_list[1]<=15 and cm_list[2]<=1 and Weight<=80:
                result['smallflag'] = 'M-S'
                if country == 'UK':
                    result['bigflag'] = 'FBA-UK-M'
                elif country == 'GER':
                    result['bigflag'] = 'FBA-GER-M'
                elif country == 'FRA':
                    result['bigflag'] = 'FBA-FRA-M'
            elif cm_list[0]<=33 and cm_list[1]<=23 and cm_list[2]<=2.5 and Weight<=460:  
                if country == 'UK':
                    result['bigflag'] = 'FBA-UK-M'
                elif country == 'GER':
                    result['bigflag'] = 'FBA-GER-M'
                elif country == 'FRA':
                    result['bigflag'] = 'FBA-FRA-M'             
                result['smallflag'] = 'M-M'
            elif cm_list[0]<=33 and cm_list[1]<=23 and cm_list[2]>2.5 and cm_list[2]<=5 and Weight<=960:
                result['smallflag'] = 'M-L1'
                if country == 'UK':
                    result['bigflag'] = 'FBA-UK-M'
                elif country == 'GER':
                    result['bigflag'] = 'FBA-GER-M'
                elif country == 'FRA':
                    result['bigflag'] = 'FBA-FRA-M'  
            elif cm_list[0]<=45 and cm_list[1]<=34 and cm_list[2]<=26 and Weight<=11900:
                if country == 'UK':
                    result['bigflag'] = 'FBA-UK-M'
                elif country == 'GER':
                    result['bigflag'] = 'FBA-GER-M'
                elif country == 'FRA':
                    result['bigflag'] = 'FBA-FRA-M'
                result['smallflag'] = 'M-L2'
            elif cm_list[0]<=61 and cm_list[1]<=46 and cm_list[2]<=46 and Weight<=1760:
                if country == 'UK':
                    result['bigflag'] = 'FBA-UK-L'
                elif country == 'GER':
                    result['bigflag'] = 'FBA-GER-L'
                elif country == 'FRA':
                    result['bigflag'] = 'FBA-FRA-L'
                result['smallflag'] = 'L-S'
            elif cm_list[0]<=120 and cm_list[1]<=60 and cm_list[2]<=60 and Weight<=29760:
                if country == 'UK':
                    result['bigflag'] = 'FBA-UK-L'
                elif country == 'GER':
                    result['bigflag'] = 'FBA-GER-L'
                elif country == 'FRA':
                    result['bigflag'] = 'FBA-FRA-L'
                result['smallflag'] = 'L-L1'
            elif cm_list[0]>120:
                if country == 'UK':
                    result['bigflag'] = 'FBA-UK-L'
                elif country == 'GER':
                    result['bigflag'] = 'FBA-GER-L'
                elif country == 'FRA':
                    result['bigflag'] = 'FBA-FRA-L'
                result['smallflag'] = 'L-L2'
        try:
            LargeCode = result['bigflag']
            SmallCode = result['smallflag']
            CURRENCYCODE_standard = cfg_standard_large_small[str(standard_id)+str(LargeCode)+str(SmallCode)+'_CURRENCYCODE']
            getprice_standard = cfg_standard_large_small[str(standard_id)+str(LargeCode)+str(SmallCode)+'_getprice']
            scope_standard = {'Weight': Weight}
            exec(getprice_standard, scope_standard)
            price_standard = scope_standard['Price']
            ex_standard = float(cfg_b_currencycode[CURRENCYCODE_standard])
            price_standard = price_standard * ex_standard #CNY
            if DestinationCountryCode == 'US':
                if cp == 'FZ':
                    price_standard = price_standard + 0.4 * float(ex_standard)
                elif cp == 'FFZ':
                    price_standard = price_standard
        except:
            profit_fba = None
            
        try:
            sum_money1 = price_first + price_standard + Money
            profit_fba = (1- kickback/100 - sum_money1/ex_standard/sellingPrice)*10.0*10.0
        except:
            profit_fba = None
        try:
            sum_money2 = price_first + price_xxj_yf + Money
            profit_qxj = (1- kickback/100 - sum_money2/ex_standard/sellingPrice)*10.0*10.0
        except:
            profit_qxj = None
        return {'profit_fba':round(profit_fba,2),'profit_qxj':round(profit_qxj,2)}
                        
#params = calculate_price(SKU='WF-2304-BK-S').calculate_profitRate_fba(sellingPrice='25.74',PackWeight='245',cm='10*10*10',logistic_way='PT',platformCountryCode='AMAZON-FBA', DestinationCountryCode='US',cp='FFZ')
#print params     
