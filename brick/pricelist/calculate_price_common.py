# -*- coding: utf-8 -*-
"""  
 @desc: 各平台算价表,总公式算价机制如下:(成本(￥)+运费(￥))/汇率/(1-利润率-平台扣点比率) = 最终售价(目标币种)
 @author: chenchen  
 @site: 
 @software: PyCharm
 @file: calculate_price.py
 @time: 2018/4/14 08:40
""" 


from django.contrib import messages
# from django.db import connection as conn


class calculate_price():
    def __init__(self,SKU,conn):
        self.SKU = SKU
        self.conn = conn
        cur = self.conn.cursor()
        try:
            sql = "SELECT CostPrice,Weight FROM py_db.b_goods WHERE SKU = '%s';"%SKU
            cur.execute(sql)
            row = cur.fetchone()
            self.Money = str(row[0])
            self.Weight = str(row[1])
        except:
            self.Money = None
            self.Weight = None
        cur.close()

    # 计算售价
    # Weight 商品原始克重(g)
    # Money  商品原始成本(人民币)
    # profitRate 利润率 默认0
    # 返回三种不同货币类型的售价,数据类型dic
    def calculate_selling_price(self,profitRate,platformCountryCode='JOOM-RUS', DestinationCountryCode='RUS',Money=None,Weight=None):
        cur = self.conn.cursor()
        try:
            Money = float(self.Money)
            Weight = float(self.Weight)
        except:
            Money = float(Money)
            Weight = float(Weight)
        profitRate = float(profitRate)

        error_info = {'error_code':200,'error_info':'信息获取成功!'}
        # 根据页面的目的地国家和平台国家编号去找物流方式编号
        sql = "SELECT logisticwaycode,logisticwaycode_desc,kickback FROM t_cfg_b_emsfare2 WHERE platform_country_code = '%s' AND countrycode = '%s'"%(platformCountryCode,DestinationCountryCode)
        cur.execute(sql)
        row = cur.fetchone()
        logisticwaycode_expression = str(row[0])
        logisticwaycode_desc = str(row[1])
        scope = {'sell_price':0,'Weight':Weight}
        exec(logisticwaycode_expression,scope)
        logisticwaycode = scope['waycode']
        #根据当前平台国家编号获取当前货币编号以及平台扣点
        kickback = float(row[2])
        CURRENCYCODE = None
        basefee = None
        try:
            sql = "SELECT basefee FROM t_cfg_platform_country WHERE platform_country_code = '%s'"%platformCountryCode
            cur.execute(sql)
            row = cur.fetchone()
            basefee = float(row[0])
            sql = "SELECT CURRENCYCODE FROM t_cfg_b_country WHERE country_code = '%s'"%DestinationCountryCode
            cur.execute(sql)
            row = cur.fetchone()
            CURRENCYCODE = str(row[0])
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = '%s'"%CURRENCYCODE
            cur.execute(sql)
            row = cur.fetchone()
            basefee = basefee * float(row[0])
        except:
            error_info = {'error_code': 2, 'error_info': '平台扣点/目的国家货币名称/ 当中没有配置！'}
            

        # 计算售价=成本价+运费
        if 1 - profitRate / 100 - kickback / 100 == 0:
            error_info = {'error_code': 7, 'error_info': '利润率和平台扣点有冲突！'}
            return

        #根据货币编号获取人民币汇率
        ExchangeRate = None
        try:
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = '%s'" %CURRENCYCODE
            cur.execute(sql)
            row = cur.fetchone()
            ExchangeRate = float(row[0])
        except:
            error_info = {'error_code': 3, 'error_info': '当前货币与人民币汇率 没有配置！'}
            

        #获取美元与人民币汇率
        ExchangeRate_USD = None
        try:
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = 'USD'"
            cur.execute(sql)
            row = cur.fetchone()
            ExchangeRate_USD = float(row[0])
        except:
            error_info = {'error_code': 4, 'error_info': '美元与人民币汇率 没有配置！'}
            

        #根据物流方式编号和目的国家编号去查询基本运费计算规则
        try:
            sql = "SELECT getprice,getprice_desc,Bracketid FROM t_cfg_b_emsfare_country2 WHERE country_code = '%s' AND logisticwaycode = '%s'"%(DestinationCountryCode,logisticwaycode)
            cur.execute(sql)
            row = cur.fetchone()
            getprice_expression = str(row[0])
            getprice_desc = str(row[1])
            scope2 = {'Weight': Weight} 
            exec(getprice_expression, scope2)
            price_yf = scope2['Price']
            Bracketid = str(row[2])
        except:
            error_info = {'error_code': 5, 'error_info': '基础费用/初始价格/初始重量/增加价格/增加重量 没有配置！'}
            
        
        #根据一次算价的物流方式得到的外键Bracketid获取分档价格
        try:
            sql = "SELECT money,CURRENCYCODE FROM t_cfg_bracket WHERE bracketid = '%s' AND weight >= '%s' ORDER BY weight LIMIT 1"%(Bracketid,Weight)
            cur.execute(sql)
            row = cur.fetchone()
            fd_money = float(row[0])
            CURRENCYCODE = str(row[1])
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = '%s'" % CURRENCYCODE
            cur.execute(sql)
            row = cur.fetchone()
            ExchangeRate2 = float(row[0])
            fd_money = fd_money * float(ExchangeRate2)
        except:
            fd_money = 0

        #一次算价,获取对应物流中文名称以及物流折扣
        logisticName = None
        Discount = None
        try:
            sql = "SELECT name,discount FROM t_cfg_b_logisticway WHERE CODE = '%s'"%logisticwaycode
            cur.execute(sql)
            row = cur.fetchone()
            logisticName = str(row[0])
            Discount = float(row[1])
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
            sql = "SELECT name,discount FROM t_cfg_b_logisticway WHERE CODE = '%s'" % pricelimit_logisticwaycode
            cur.execute(sql)
            row = cur.fetchone()
            logisticName = str(row[0])
            Discount = float(row[1])
        except:
            logisticName = None
            Discount = None
        #二次算价获取运费
        sql = "SELECT getprice,getprice_desc,Bracketid FROM t_cfg_b_emsfare_country2 WHERE country_code = '%s' AND logisticwaycode = '%s'" % (DestinationCountryCode, pricelimit_logisticwaycode)
        cur.execute(sql)
        row = cur.fetchone()
        getprice_expression = str(row[0])
        getprice_desc = str(row[1])

        scope4 = {'Weight': Weight} 
        exec(getprice_expression,scope4)
        price_yf = scope4['Price']
        Bracketid = str(row[2])
        #二次算价获取分档运费
        try:
            sql = "SELECT money,CURRENCYCODE FROM t_cfg_bracket WHERE bracketid = '%s' AND weight >= '%s' ORDER BY weight LIMIT 1"%(Bracketid,Weight)
            cur.execute(sql)
            row = cur.fetchone()
            fd_money = float(row[0])
            CURRENCYCODE = str(row[1])
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = '%s'" % CURRENCYCODE
            cur.execute(sql)
            row = cur.fetchone()
            ExchangeRate2 = float(row[0])
            fd_money = fd_money * float(ExchangeRate2)
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
        cur.close()
        # conn.close()
        return params

    # 计算利润率
    # platformCountryCode=t_cfg_b_emsfare.platform_country_code
    # Weight 商品原始克重(g)
    # Money  商品原始成本(人民币)
    # sellingPrice 售价(人民币，显示的是加入汇率计算)
    # 返回profitRate利润率(百分制,15就是 15%)
    #(成本(￥)+运费(￥))/汇率/(1-利润率-平台扣点比率) = 最终售价(目标币种)
    def calculate_profitRate(self, sellingPrice,platformCountryCode='JOOM-RUS', DestinationCountryCode='RUS',Money=None,Weight=None):
        cur = self.conn.cursor()
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
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = 'USD'"
            cur.execute(sql)
            row = cur.fetchone()
            ExchangeRate_USD = float(row[0])
        except:
            ExchangeRate_USD = None
        #根据当前平台国家编号获取当前货币编号以及平台扣点
        try:
            sql = "SELECT basefee FROM t_cfg_platform_country WHERE platform_country_code = '%s'"%platformCountryCode
            cur.execute(sql)
            row = cur.fetchone()
            basefee = float(row[0])
            sql = "SELECT kickback FROM t_cfg_b_emsfare2 WHERE platform_country_code = '%s' AND countrycode = '%s'"%(platformCountryCode,DestinationCountryCode)
            cur.execute(sql)
            row = cur.fetchone()
            kickback = float(row[0])
            sql = "SELECT CURRENCYCODE FROM t_cfg_b_country WHERE country_code = '%s'"%DestinationCountryCode
            cur.execute(sql)
            row = cur.fetchone()
            CURRENCYCODE = str(row[0])
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = '%s'"%CURRENCYCODE
            cur.execute(sql)
            row = cur.fetchone()
            ExchangeRate_basefee = row[0]
            basefee = basefee * float(ExchangeRate_basefee)
        except:
            kickback = None
            CURRENCYCODE = None
            basefee = None
        #根据货币编号获取人民币汇率
        try:
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = '%s'"%CURRENCYCODE
            cur.execute(sql)
            row = cur.fetchone()
            ExchangeRate = float(row[0])
        except:
            ExchangeRate = None
       # 根据页面的目的地国家和平台国家编号去找默认物流方式编号，最大价格限制以及超过最大价格后采取的新的物流方式编号
        sql = "SELECT logisticwaycode FROM t_cfg_b_emsfare2 WHERE platform_country_code = '%s' AND countrycode = '%s'"%(platformCountryCode,DestinationCountryCode)
        cur.execute(sql)
        row = cur.fetchone()
        logisticwaycode_expression = str(row[0])
        scope = {'sell_price':sellingPrice,'Weight':Weight}
        exec(logisticwaycode_expression,scope)
        waycode = scope['waycode']
                
        try:
            sql = "SELECT name,discount FROM t_cfg_b_logisticway WHERE CODE = '%s'" % waycode
            cur.execute(sql)
            row = cur.fetchone()
            logisticName = str(row[0])
            Discount = float(row[1])
        except:
            logisticName = None
            Discount = None
        # 根据物流方式编号和目的国家编号去查询基本运费计算规则
        sql = "SELECT getprice,Bracketid FROM t_cfg_b_emsfare_country2 WHERE country_code = '%s' AND logisticwaycode = '%s'" % (DestinationCountryCode, waycode)
        cur.execute(sql)
        row = cur.fetchone()
        getprice_expression = str(row[0])
        scope2 = {'Weight': Weight} 
        exec(getprice_expression,scope2)
        price_yf = scope2['Price']
        Bracketid = str(row[1])
        #二次算价获取分档运费
        try:
            sql = "SELECT money,CURRENCYCODE FROM t_cfg_bracket WHERE bracketid = '%s' AND weight >= '%s' ORDER BY weight LIMIT 1"%(Bracketid,Weight)
            cur.execute(sql)
            row = cur.fetchone()
            fd_money = float(row[0])
            CURRENCYCODE = str(row[1])
            sql = "SELECT ExchangeRate FROM t_cfg_b_currencycode WHERE CURRENCYCODE = '%s'" % CURRENCYCODE
            cur.execute(sql)
            row = cur.fetchone()
            ExchangeRate = row[0]
            fd_money = fd_money * float(ExchangeRate)
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
        cur.close()
        return params
